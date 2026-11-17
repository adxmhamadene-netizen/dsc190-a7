from pathlib import Path
import pandas as pd

IN = Path("data/clean/events.csv")
OUT = Path("data/transformed/events.csv")


def main():
    df = pd.read_csv(IN, dtype={"duration_seconds": int})
    df["date"] = df["timestamp"].str[:10]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"transform: {len(df)} rows -> {OUT}")


if __name__ == "__main__":
    main()
