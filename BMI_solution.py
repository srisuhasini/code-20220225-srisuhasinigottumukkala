import pandas as pd
import numpy as np
import argparse
import json

bmitable = [{"BMI_Category": "Under Weight","BMI_Range_low":0, "BMI_Range_high":18.4,"risk":"Malnutrition risk"},
            {"BMI_Category": "Normal Weight","BMI_Range_low":18.5, "BMI_Range_high":24.9,"risk":"Low risk"},
            {"BMI_Category": "Over Weight","BMI_Range_low":25, "BMI_Range_high":29.9,"risk":"Enhanced risk"},
            {"BMI_Category": "Moderately Obese","BMI_Range_low":30, "BMI_Range_high":34.9,"risk":"Medium risk"},
            {"BMI_Category": "Severely Obese","BMI_Range_low":35, "BMI_Range_high":39.9,"risk":"High risk"},
            {"BMI_Category": "Very Severely Obese","BMI_Range_low":40, "BMI_Range_high":10000,"risk":"Very high risk"}]

def calculate_BMI(jsondata):
    for data in jsondata:
        mass = data["WeightKg"]
        height = data["HeightCm"]/100
        bmi = np.round(mass/(height*height),2)
        btab = [b for b in bmitable if (b["BMI_Range_low"] <= bmi) and (bmi <= b["BMI_Range_high"])]
        data["BMI"] = bmi
        data["BMI_Category"] = btab[0]["BMI_Category"]
        data["Health_risk"] = btab[0]["risk"]
    return jsondata

def find_overweight(jsondata):
    over_weights = [x for x in jsondata if x["BMI_Category"] in ["Over Weight","Moderately Obese","Severely Obese","Very Severely Obese"]]
    male_overweights = len([x for x in over_weights if x["Gender"] == "Male"])
    female_overweights = len([x for x in over_weights if x["Gender"] == "Female"])
    print("Number of people with overweight:"+ str(len(over_weights)))
    pmale =  (male_overweights/len(over_weights))*100
    print("Percentage of males overweight is:"+ str(round(pmale,2)))
    pfemale =  (female_overweights/len(over_weights))*100
    print("Percentage of females overweight is:"+ str(round(pfemale,2)))
    pmale_all = (male_overweights/len(jsondata))*100
    print("Percentage of males overweight in whole data is:"+ str(round(pmale_all,2)))
    pfemale =  (female_overweights/len(jsondata))*100
    print("Percentage of males overweight in whole data is"+ str(round(pfemale,2)))
    return over_weights
if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
                description='Command Line for ESP Event Detection!!')
    PARSER.add_argument('-i', '--input_json_file_path', type=str,
                        help='Input file', required=True)
    PARSER.add_argument('-o', '--output_json_file_path', type=str,
                        help='Input file', required=True)
    ARGS = PARSER.parse_args()
    INPATH = ARGS.input_json_file_path.replace("/", "\\")
    OUTPATH = ARGS.output_json_file_path.replace("/", "\\")
    f = open(INPATH)
    jsondata = json.load(f)
    jsondata = calculate_BMI(jsondata)
    with open(OUTPATH + "\\bmi.json", "w") as outfile:
        json.dump(jsondata, outfile)
    over_weights = find_overweight(jsondata)
    with open(OUTPATH + "\\overweightdata.json", "w") as outfile2:
        json.dump(over_weights, outfile2)


