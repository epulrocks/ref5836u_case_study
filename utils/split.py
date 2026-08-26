import pandas as pd

def split(df, original_df):
	accepted_df = df.loc[df["rejected"]==False]
	rejected_df = df.loc[df["rejected"]==True]		
	additional_col = [i for i in rejected_df.columns if i not in original_df.columns]
	original_rejected_df = pd.concat([original_df.loc[rejected_df.index], rejected_df[additional_col]], axis=1)
	return (accepted_df, original_rejected_df)
