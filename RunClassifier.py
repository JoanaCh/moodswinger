import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler




def leEClassifica:

	# Wait 30 seconds

	# Bitalino reads the eeg
	# Biosppy processes the result
	# Pass the result into a Dataframe called data

	###Process the Dataframe data to enter into the Classifier###

	#Necessary if the number complex columns still exist
	data = data.drop(['theta_fft', 'alpha_low_fft', 'alpha_high_fft', 'beta_fft', 'gamma_fft'], axis=1)

	scaler = StandardScaler()
	data = scaler.fit_transform(data)

	# Load Classifier
	with open('eeg_classifier.pkl', 'rb') as fid:
    		clf = pickle.load(fid)

    	# Gives an array with state for each sample(row)  
    	result = clf.predict(data)

    	# If you want to predict from the first sample(row)
    	state = result[0]

    	return state


