from generate_booster_v2 import generate_booster
import time
    
# def lambda_handler(event, context):
t0 = time.time()
booster = generate_booster("MKM")
print (booster)

headers = {
  'Content-Type': 'application/json',
  "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,X-Amz-Security-Token,Authorization,X-Api-Key,X-Requested-With,Accept,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Allow-Headers",
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "*",
  "X-Requested-With": "*"
}

body = {
  "cards": booster
}

response = {
  "headers": headers,
  "body": body
}

# return booster

print(f"{str(time.time() - t0)[:5]} seconds to run function")



# https://stackoverflow.com/questions/5324647/how-to-merge-a-transparent-png-image-with-another-image-using-pil
