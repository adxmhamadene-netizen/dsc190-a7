from pathlib import Path
import pandas as pd

IN = Path("data/transformed/events.csv")
OUT = Path("data/features/events.csv")


def main():
    df = pd.read_csv(IN, dtype={"duration_seconds": int})
    df["duration_minutes"] = df["duration_seconds"] / 60
    df["weekday"] = pd.to_datetime(df["date"], format="%Y-%m-%d").dt.day_name()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"features: {len(df)} rows -> {OUT}")


if __name__ == "__main__":
    main()
