# Demo Notes — Power Generation Forecasting & Variance Explanation Agent

## Project Links

- Live API: https://web-production-85961.up.railway.app/api/demo
- API Documentation: https://web-production-85961.up.railway.app/docs
- GitHub Repository: https://github.com/pavanenti18/generation-forecasting-variance-agent

## Demonstration

1. Enter weather conditions, outage status, and the supplied generation forecast.
2. Submit the inputs to the API.
3. View predicted generation and compare it with the supplied forecast.
4. Provide actual generation to calculate forecast error and obtain a rule-based explanation.

## Example Results

- Predicted generation: 12.73 MWh
- Supplied forecast: 21.36 MWh
- Prediction minus supplied forecast: -8.63 MWh
- Actual generation: 4.19 MWh
- Actual forecast error: -17.17 MWh (overforecast)

## Evaluation

The project includes model evaluation metrics, a baseline comparison, and automated tests.

## Limitations

- The dataset is small and synthetic.
- Linear Regression is used as a baseline model.
- Explanations are rule-based diagnostic hints, not proven causal findings.
- An LLM and RAG workflow are not implemented.
