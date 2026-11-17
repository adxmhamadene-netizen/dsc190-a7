from pathlib import Path
import pandas as pd

IN = Path("data/raw/events.csv")
OUT = Path("data/clean/events.csv")

VALID_EVENTS = {"click", "login", "purchase", "scroll", "view"}
FORMATS = [
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%m/%d/%Y %H:%M:%S",
]


def parse_timestamps(s: pd.Series) -> pd.Series:
    out = pd.Series(pd.NaT, index=s.index, dtype="datetime64[ns]")
    for fmt in FORMATS:
        parsed = pd.to_datetime(s, format=fmt, errors="coerce")
        out = out.fillna(parsed)
    return out


def main():
    df = pd.read_csv(IN, dtype=str)

    df = df.dropna()
    df = df[df["event_type"].isin(VALID_EVENTS)]

    df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")
    df = df[df["duration_seconds"] > 0]

    ts = parse_timestamps(df["timestamp"])
    df = df[ts.notna()]
    df["timestamp"] = ts[ts.notna()].dt.strftime("%Y-%m-%dT%H:%M:%S")

    df["duration_seconds"] = df["duration_seconds"].astype(int)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"clean: {len(df)} rows -> {OUT}")


if __name__ == "__main__":
    main()
