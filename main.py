from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Function to check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to check if a number is an Armstrong number
def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

# Function to check if a number is a Perfect number
def is_perfect(n):
    return n == sum(i for i in range(1, n) if n % i == 0)

@app.get("/api/classify-number")
def classify_number(number: int = Query(..., description="Enter an integer")):
    # Define properties (Even/Odd, Armstrong)
    properties = ["even" if number % 2 == 0 else "odd"]
    if is_armstrong(number):
        properties.insert(0, "armstrong")  # Armstrong comes first if true

    # Get a fun fact about the number
    try:
        fun_fact = requests.get(f"http://numbersapi.com/{number}/math").text
    except:
        fun_fact = "Fun fact not available."

    # JSON Response
    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(map(int, str(number))),
        "fun_fact": fun_fact
    }
    
    return response
