# PRD: Used-Car Price Estimator

## Problem
Buyers and sellers of used cars have no quick way to check whether a asking price is fair. They guess, overpay, or underprice their own car.

## Who It's For
- People shopping for a used car who want a sanity check on a listing price.
- Private sellers deciding what price to ask.

## Goals
- A user enters a car's brand, model, year, mileage, fuel type, and transmission, and gets a fair-price estimate in seconds.
- Estimates are grounded in real listings, not guesswork.

## Scope
In scope:
- Price estimates for cars similar to those in our dataset (`used-cars.csv`: ~3,900 real listings, 56 brands, model years 1998–2024, prices $2,000–$250,000).
- A simple interface: enter the six car details, see an estimated price.
- Clear messaging when the entered car is unlike anything in the data (estimate may be unreliable).

Out of scope:
- Real-time market listings or live price feeds.
- Guaranteed sale prices or negotiation advice.
- Non-car vehicles, salvage/auction pricing, and financing or insurance features.

## How We'll Know It Works
- Estimates for typical cars fall within the price range of similar listings in the dataset.
- A test set of listings held back from model training is predicted with reasonable average error.
- A new user can go from opening the app to seeing an estimate with no instructions.
