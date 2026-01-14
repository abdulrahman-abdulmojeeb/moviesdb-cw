FROM oven/bun:1-alpine

WORKDIR /app

COPY package.json bun.lock* ./
RUN bun install --frozen-lockfile || bun install

COPY . .

RUN adduser -D appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5173

CMD ["bun", "run", "dev"]
