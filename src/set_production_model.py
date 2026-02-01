import argparse
from src.registry_manager import (
    set_production_model,
    lock_production,
    unlock_production
)

parser = argparse.ArgumentParser()
parser.add_argument("--set", help="Experiment ID to set as production")
parser.add_argument("--lock", action="store_true")
parser.add_argument("--unlock", action="store_true")

args = parser.parse_args()

if args.set:
    set_production_model(args.set)
    print(f"Production model set to {args.set}")

if args.lock:
    lock_production()
    print("Production model LOCKED")

if args.unlock:
    unlock_production()
    print("Production model UNLOCKED")
