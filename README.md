# Interview Recording File Management Automator

## Test usage

Create a `.env` file and add this content
```text
SOURCE_DIRECTORY=./test_dir
DESTINATION_DIRECTORY=./test_output_dir
REMOTASKS_EMAIL=test@work.com
TARGET_FILE_SUBSTRING=video
GOOGLE_DRIVE_URL=https://drive.google.com/
```

Install packages and run
```bash
# Set up venv first if you want

pip3 install -r requirements.txt

python3 main.py mystr test@gmail.com
```

You should see the outputted file in the `test_output_dir` directory with the proper naming convention!
