import requests
import sys
import os

# Raw URL of the text files for reference
hpp1_url = "https://raw.githubusercontent.com/kevlaria/Harry-Potter/master/HarryPotterNLP/HP1.txt"
hpc1_url = "https://raw.githubusercontent.com/amephraim/nlp/master/texts/J.%20K.%20Rowling%20-%20Harry%20Potter%201%20-%20Sorcerer%27s%20Stone.txt"

def download_text_file(url, output_file):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error if status is not 200
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"File successfully downloaded and saved as '{output_file}'")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def main():
    os.makedirs("./assets", exist_ok=True)
    download_text_file(hpp1_url, "./assets/hpp1.txt")
    download_text_file(hpc1_url, "./assets/hpc1.txt")


if __name__ == "__main__":
    main()