FROM eclipse-temurin:17-jre-alpine

LABEL version="1.0"
LABEL description="Java Calculator"

WORKDIR /app

COPY calc.java /app/

RUN javac calc.java

CMD ["java", "calc"]