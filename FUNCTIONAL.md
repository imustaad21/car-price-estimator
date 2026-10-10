# Functional Requirements: Used-Car Price Estimator

## Inputs
The user provides the following, matching the columns in `used-cars.csv`:

- **brand** (required): one of the 56 brands in the dataset (e.g. Ford, Toyota, BMW, Honda). Free text with suggestions; unknown brands are rejected with guidance.
- **model** (required): free text (e.g. "Camry 2.5L LE"). Matched loosely against dataset models since naming is inconsistent.
- **year** (required): whole number, 1998–2024 (the dataset's range).
- **mileage_miles** (required): whole number, 100–300,000 miles (the dataset's range).
- **fuel_type** (required): one of Diesel, E85 Flex Fuel, Gasoline, Hybrid, Plug-In Hybrid. `Unknown` means the user doesn't know; the estimate then uses the average across fuel types.
- **transmission** (required): free text matched loosely (the dataset has 60 variants, e.g. `A/T`, `8-Speed A/T`, `Automatic`, `6-Speed M/T`). Common synonyms (automatic, manual, CVT) are accepted and mapped to the closest dataset terms.
- **accident_reported** (optional, defaults to `No`): Yes or No.
- **clean_title** (optional, defaults to `Yes`): Yes, or Unknown if the user is unsure.

All required fields must be filled before an estimate is shown. Invalid entries (year 1890, negative mileage, empty brand) are rejected with a plain-language message naming the accepted range.

## Output
For a valid car, the app shows:

1. **Estimated price**: a single dollar figure (e.g. $14,500).
2. **Low–high range**: a band around the estimate (e.g. $13,000–$16,000) reflecting how much similar listings vary.
3. **Top factors**: the 2–3 inputs that moved the price most for this car, each with a short explanation (e.g. "High mileage (198,000 mi) lowered the estimate" or "Accident reported lowered the estimate").

## Unusual Inputs
- **Very old car (year near or below 1998)**: accepted down to 1998; anything older is rejected as outside the data, with a message saying the estimate would be unreliable.
- **Very high mileage (near or above 300,000)**: accepted up to 300,000 with a warning that few comparable listings exist, so the range is wider. Above 300,000 is rejected as outside the data.
- **Brand or model with few comparables** (rare brands such as Karma, Lucid, Maybach): the app still estimates but flags it as low-confidence with a wider range.
- **Unknown fuel type / Unknown title**: the estimate proceeds using dataset averages for those fields, and the result notes this assumption.

## Examples
1. **Typical car — 2015 Acura ILX, 75,000 miles, Gasoline, 5-Speed A/T, no accident, clean title.** Expected: an estimate near the middle of similar ILX listings (around $14,000–$15,000), a normal-width range, and factors naming year and mileage as the main drivers.
2. **High-mileage older car — 2013 Acura ILX, 198,000 miles, Gasoline, automatic-type transmission, accident reported.** Expected: a noticeably lower estimate (around $10,000–$11,000), with top factors calling out high mileage and the accident report as the reasons.
3. **Edge case — 2001 car with 290,000 miles.** Expected: an estimate is still returned (both values are inside the data range) but with a low-confidence flag and a wide range, warning that very few comparable listings exist.
