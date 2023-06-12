FROM --platform=linux/amd64 ghcr.io/owl-corp/python-poetry-base:3.11-slim

# Install dependencies
WORKDIR /app
COPY pyproject.toml poetry.lock .env ./
RUN poetry install

# Generate prisma client
COPY prisma ./prisma
RUN poetry run prisma generate

# Copy the rest of the project code
COPY . .

# Start the bot
ENTRYPOINT ["poetry", "run"]
CMD ["python", "-m", "src"]
