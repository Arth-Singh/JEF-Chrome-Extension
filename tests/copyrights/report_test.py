import unittest
import tempfile
import os
import jef
from jef.copyrights import report
from jef.copyrights import score


class TestReport(unittest.TestCase):

    def test_report(self):
        """Test report generation functionality"""
        submission = "This is a test sentence. This is unique content. This is copied exactly."
        reference = "Something different here. More unique text. This is copied exactly."

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tf:
            report_path = tf.name

        try:
            _score = score(submission, reference)
            report.generate(_score, submission, reference, report_path)

            # Verify report was created and contains expected sections
            with open(report_path, 'r') as f:
                report_content = f.read()
                print(report_content)

            self.assertIn("Copyright Analysis Report", report_content)
            self.assertIn("Overall Copyright Risk Score", report_content)
            self.assertIn("Individual Method Scores", report_content)
            self.assertIn("N-gram Analysis", report_content)
            self.assertIn("Legend", report_content)
            self.assertIn("Analyzed Text", report_content)
        finally:
            os.unlink(report_path)

if __name__ == '__main__':
    unittest.main()