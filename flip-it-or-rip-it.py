from generate_booster import generate_booster
import time

t0 = time.time()

booster = generate_booster('MH2')

print(f"{str(time.time() - t0)[:5]} seconds to run function")