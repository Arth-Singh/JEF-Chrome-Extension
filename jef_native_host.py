#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3
import json
import struct
import sys
import os
import subprocess
import tempfile
import traceback

# Log file for debugging
LOG_FILE = '/tmp/jef_native_host.log'

def log(message):
    """Write debug messages to log file."""
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(f"{message}\n")
    except:
        pass

def get_message():
    """Read a message from Chrome using native messaging protocol."""
    raw_length = sys.stdin.buffer.read(4)
    if len(raw_length) == 0:
        sys.exit(0)
    message_length = struct.unpack('@I', raw_length)[0]
    message = sys.stdin.buffer.read(message_length).decode('utf-8')
    return json.loads(message)

def send_message(message):
    """Send a message to Chrome using native messaging protocol."""
    encoded_message = json.dumps(message).encode('utf-8')
    sys.stdout.buffer.write(struct.pack('@I', len(encoded_message)))
    sys.stdout.buffer.write(encoded_message)
    sys.stdout.buffer.flush()

def run_jef_test(command, text):
    """Run JEF test command with the provided text."""
    try:
        # TODO: Update this path to point to your JEF installation
        jef_path = '/path/to/your/jef/installation'
        
        # Check if JEF directory exists
        if not os.path.exists(jef_path):
            return {'error': f'JEF directory not found: {jef_path}'}
        
        # Write text to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(text)
            temp_file_path = temp_file.name
        
        try:
            # Use the Python from the virtual environment
            # TODO: Update this path to point to your JEF virtual environment
            python_path = os.path.expanduser('~/jef_env/bin/python')
            
            # Check if virtual environment exists
            if not os.path.exists(python_path):
                # Fallback to system Python
                python_path = sys.executable
            
            # Read the file content since JEF CLI expects text, not file path
            with open(temp_file_path, 'r') as f:
                file_content = f.read()
            
            cmd = [python_path, '-m', 'jef.cli', command, file_content]
            
            log(f"Running command: {' '.join(cmd)}")
            
            # Set PYTHONPATH to include JEF directory
            env = os.environ.copy()
            env['PYTHONPATH'] = jef_path
            
            result = subprocess.run(
                cmd,
                cwd=jef_path,
                capture_output=True,
                text=True,
                env=env
            )
            
            log(f"Return code: {result.returncode}")
            log(f"Stdout: {result.stdout}")
            log(f"Stderr: {result.stderr}")
            
            if result.returncode != 0:
                return {'error': f'JEF command failed: {result.stderr}'}
            
            # JEF outputs human-readable text, not JSON
            # Let's parse the output to extract the key information
            output = result.stdout
            
            # Log the raw output for debugging
            log(f"Raw JEF output:\n{output}\n{'='*50}")
            
            # Initialize result structure
            result_data = {
                'score': 0.0,
                'percentage': 0.0,
                'total_possible_score': 0,
                'missing': [],
                'matches': []
            }
            
            # Parse the output
            lines = output.split('\n')
            for i, line in enumerate(lines):
                if 'Score:' in line and '%' in line:
                    # Extract percentage
                    try:
                        percentage = float(line.split(':')[1].strip().replace('%', ''))
                        result_data['percentage'] = percentage
                    except:
                        pass
                elif 'Raw Score:' in line:
                    try:
                        result_data['score'] = float(line.split(':')[1].strip())
                    except:
                        pass
                elif 'Max Possible:' in line:
                    try:
                        result_data['total_possible_score'] = int(line.split(':')[1].strip())
                    except:
                        pass
                elif line.strip().startswith('•'):
                    # Handle bullet points for missing elements
                    missing_text = line.strip()[1:].strip()  # Remove bullet and whitespace
                    if missing_text:
                        result_data['missing'].append(missing_text)
                elif '✅' in line:
                    # Handle checkmarks for found elements
                    found_text = line.split('✅')[1].strip()
                    if found_text:
                        result_data['matches'].append(found_text)
            
            # For JEF score command, extract individual test scores
            if command == 'jef_score' or command == 'jef_calculator':
                if 'Tiananmen Score:' in output:
                    try:
                        result_data['tiananmen_score'] = float(output.split('Tiananmen Score:')[1].split()[0])
                    except:
                        pass
                if 'Nerve Agent Score:' in output:
                    try:
                        result_data['nerve_agent_score'] = float(output.split('Nerve Agent Score:')[1].split()[0])
                    except:
                        pass
                if 'Methamphetamine Score:' in output:
                    try:
                        result_data['meth_score'] = float(output.split('Methamphetamine Score:')[1].split()[0])
                    except:
                        pass
                if 'Harry Potter Score:' in output:
                    try:
                        result_data['harry_potter_score'] = float(output.split('Harry Potter Score:')[1].split()[0])
                    except:
                        pass
            
            return {'result': result_data}
        
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    except Exception as e:
        log(f"Error in run_jef_test: {traceback.format_exc()}")
        return {'error': str(e)}

def main():
    log("Native host started")
    try:
        while True:
            try:
                message = get_message()
                log(f"Received message: {message}")
                
                command = message.get('command')
                text = message.get('text', '')
                
                if command and text:
                    response = run_jef_test(command, text)
                    send_message(response)
                else:
                    send_message({'error': 'Invalid request: missing command or text'})
            
            except Exception as e:
                log(f"Error in main loop: {traceback.format_exc()}")
                send_message({'error': str(e)})
    except Exception as e:
        log(f"Fatal error: {traceback.format_exc()}")

if __name__ == '__main__':
    main()