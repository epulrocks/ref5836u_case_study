import os
from google import genai
from .model import CategoryMap
from time import sleep

def classify(df, db):
	freetext_list = df["business_category_freetext"].dropna().unique()
	category_list = db.query("SELECT canonical_name from categories")["canonical_name"].tolist()
	catmap = get_classification_map(freetext_list, category_list)
	df["canonical_category"] = df["business_category_freetext"].apply(
		lambda x: catmap.get(x, None)
	)

def get_classification_map(freetext_list, category_list):
	client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
	prompt = f"""
	Classify the following 'business_category_freetext' into one of the
	following 'canonical_category'.
	If none of the 'canonical_category' is suitable, remove from the output.
	Do not change the spellings or case of both the
	'business_category_freetext' and 'canonical_category'.

	business_category_freetext: 
	{"\n".join(freetext_list)}

	canonical_category:
	{"\n".join(category_list)}
	"""
	retryCount = 0
	while retryCount < 3:
		try:
			retryCount += 1
			response = client.models.generate_content(
				model="gemini-3.6-flash",
				contents=prompt,
				config={
					"response_mime_type": "application/json",
					"response_schema": list[CategoryMap],
				},
			)
			return {
				catmap.freetext: catmap.canonical_category for catmap in response.parsed
			}
		except genai.errors.APIError as e:
			if e.code == 429:
				delay = 30
				for detail in e.details.get("error", {}).get("details", []):
					if 'retryDelay' in detail:
						delay_str = detail['retryDelay']
						# plus 10% buffer
						delay = float(delay_str.replace('s', '')) * 1.1
						break
				sleep(delay)
			else:
				raise e
	raise Exception("Failed to classify after 3 attempts")