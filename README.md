# ref5836u_case_study

## Technical Notes
Recommended Python version 3.12.
Other version might work but not tested.

For the AI part of the project, I am using Gemini API, so we do need the Gemini API key to run. We can use the free tier but the quota is a bit limited. Do note that this script consumes quota every each run, so be mindful during testing this script.

## Obtaining Gemini API Key
I already had my key, so I won't be able to accurately explain the steps. But the steps should be something like this:
1) Login to [aistudio.google.com](https://aistudio.google.com)
2) Go to 'API Keys' in left menu, or, go to this link: [https://aistudio.google.com/api-keys](https://aistudio.google.com/api-keys)
3) Click on 'Create New API Key' on top right
4) Give a name to your key and choose cloud project to assign to
5) Copy the API key to be used in .env

## How to use

1) Clone the repository:
```bash
git clone git@github.com:epulrocks/ref5836u_case_study.git
```

2) CD into project folder:
```bash
cd ref5836u_case_study
```

3) Unzip 'case_study.zip' into project folder. This is the zip that includes 'reference.db' and 'data' folder containing the input csv files

4) Setup config.yaml, depending on where 'reference.db' and 'data' folder is located. "./" means current folder

5) Set up Environment Variable for the GEMINI_API_KEY, or, just use .env:
	- Replace the placeholder API key inside .env.example
	- Rename .env.example to .env

6) Setup Virtual Environment and install dependencies:
	- Linux:
	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt
	```
	- Windows (cmd):
	```cmd
	python -m venv .venv
	.venv\Scripts\activate.bat
	pip install -r requirements.txt
	```

7) Run the program:
	- Linux:
	```bash
	python3 consolidate.py
	```
	- Windows (cmd):
	```cmd
	python consolidate.py
	```

## Architecture Decisions
Python pandas library is largely used for the Data Transformation process as it is very easy to use and the functions are simple and has very good readability. I could have used the builtin csv library for speed, but using pandas keeps this script easy to adapt if we were to include other file extension like excel, json, etc.

Yaml is used for the config file format for its easy to read and modify structure, as the target user for this script is non-technical associates. We dont have much settings to configure for now, but I would like to prepare if this project were to scale larger.

For the categorization process, currently it is fully dependent on LLM (Gemini API) to map the freetext into canonical category. We do have other alternative like ChatGPT or Deepseek, but so far I only have experience using Gemini API. In other words, I am not saying Gemini is the best or cheapest, but it works for this project.

## Data Processing Decisions
There is some assumption I made to simplify the process:
	- Similar merchant_name but with different business type (Sdn. Bhd., Holdings, Tradings, etc.) are always considered different company
	- Same merchant_name but different info (region, category, contact, etc.) are considered as same company.
	- Regions are not interpreted or mapped to canonical regions. e.g. Klang Valley or KL are not mapped to Central

The process flow is as follows:
1) Combine all data csv into one dataframe
2) Normalize the data: Strip whitespace, Fix case, Standardize phone number
3) Classify business categories using LLM
4) Validate info if its valid
5) Deduplicate. In this process, I had to make some judgement calls:
	- In some cases same merchant name with multiple submission, there will be mixed of accepted and rejected submission. Initially I was planning on combining those rejected submissions with their accepted submissions, which means that they will not appear in the errors.csv. However in the BRIEF.md, it is mention that it should contain every rejected submission. So I decided to just list all those error rows even if the same merchant has an accepted submission.
	- In short, basically the list of submissions are split into accepted and rejected, before we deduplicate the accepted list
6) Output to clean.csv and errors.csv
	- As mentioned in BRIEF.md, clean.csv and errors.csv has some differences
	- clean.csv contains only accepted submissions, completed with normalization, validation, and deduplication
	- errors.csv contains rejected rows with the exact same info from the input file. In other words, before normalization, validation, and deduplication.
	- I believe it is best to keep the information as original so that it mirrors what the data received from the submissions, to ensure that the PIC checking on unmodified data as reference.

## Scalability
### Input
Currently, the input process of this automation is limited to reading file csv from a folder, and it is limited to how much RAM does the host/running device has. As mentioned in BRIEF.md, the script should process all partners in "one run". If the total size of input file exceeds the RAM, this code would encounter error. Some modification I had in mind is by implementing reading file by chunk and collect the results in a temp database. We can produce the output after all chunks have been processed.

### Classification with AI
With the current implementation of classification using LLM on each run, it might cost a lot if this were to scale. We can reduce this cost by implementing cache or database of previously classified freetext categories so that we can map the categories using past data first. Also, if we have a large set of data categories mapping, we could actually build a model using machine learning. Recently I discovered about a service called AWS Comprehend which is a platform for training our own classification model. Honestly this is something I have no experience in, but it might be worth the research.

### Implementing Recurring Pipeline
Some points worth research on:
	- Hosting the script to cloud such as AWS Lambda where it was designed to scale depending on realtime workload
	- If the reference.db was meant to grow, it should be hosted on a cloud database so that different person running the automation will always refer to the same updated database