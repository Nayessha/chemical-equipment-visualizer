import pandas as pd

def analyze_csv(file):
    df = pd.read_csv(file)

    type_distribution = df["Type"].value_counts().to_dict()

    summary = {
        "total_equipment": len(df),
        "average_flowrate": df["Flowrate"].mean(),
        "average_pressure": df["Pressure"].mean(),
        "average_temperature": df["Temperature"].mean(),
        "equipment_type_distribution": type_distribution
    }

    return summary, df
