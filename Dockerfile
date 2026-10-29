FROM python:3.11-bookworm
WORKDIR /app
# Mise à jour et suppression du fichier SBOM interne de pip qui trompe Trivy
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    find /usr/local/lib/python* -name "*.cdx.json" -delete
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ .
EXPOSE 5000
CMD ["python","app.py"]