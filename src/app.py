import os
import socket
import datetime
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Production CI/CD Pipeline - Abdelali Kholty</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0b0f19;
            --card-bg: rgba(22, 30, 49, 0.75);
            --card-border: rgba(255, 255, 255, 0.08);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --primary: #3b82f6;
            --primary-glow: rgba(59, 130, 246, 0.25);
            --success: #10b981;
            --success-glow: rgba(16, 185, 129, 0.2);
            --accent: #8b5cf6;
        }
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        body {
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(139, 92, 246, 0.15) 0px, transparent 50%);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem 1rem;
        }
        .container {
            width: 100%;
            max-width: 900px;
        }
        .card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            padding: 3rem 2.5rem;
            backdrop-filter: blur(16px);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }
        .badge-live {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--success-glow);
            color: var(--success);
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
        }
        .pulse-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--success);
            box-shadow: 0 0 12px var(--success);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.3); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.8; }
        }
        h1 {
            font-size: 2.6rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 1.2;
            background: linear-gradient(135deg, #ffffff 40%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.75rem;
        }
        .subtitle {
            color: var(--text-muted);
            font-size: 1.15rem;
            line-height: 1.6;
            margin-bottom: 2.5rem;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1.25rem;
            margin-bottom: 2.5rem;
        }
        .stat-box {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--card-border);
            padding: 1.25rem;
            border-radius: 16px;
            transition: transform 0.2s, border-color 0.2s;
        }
        .stat-box:hover {
            transform: translateY(-3px);
            border-color: rgba(59, 130, 246, 0.4);
        }
        .stat-title {
            color: var(--text-muted);
            font-size: 0.8rem;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }
        .stat-value {
            font-size: 1.1rem;
            font-weight: 700;
            color: #fff;
        }
        .tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 2.5rem;
        }
        .tag {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--card-border);
            padding: 6px 14px;
            border-radius: 10px;
            font-size: 0.85rem;
            font-weight: 500;
            color: #cbd5e1;
        }
        .actions {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 22px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.95rem;
            text-decoration: none;
            transition: all 0.2s ease;
            cursor: pointer;
        }
        .btn-primary {
            background: var(--primary);
            color: #fff;
            box-shadow: 0 4px 14px var(--primary-glow);
        }
        .btn-primary:hover {
            background: #2563eb;
            transform: translateY(-2px);
        }
        .btn-secondary {
            background: rgba(255, 255, 255, 0.06);
            color: #f1f5f9;
            border: 1px solid var(--card-border);
        }
        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-2px);
        }
        footer {
            margin-top: 2rem;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.85rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="badge-live">
                <span class="pulse-dot"></span>
                <span>Déployé avec Succès sur AWS EKS</span>
            </div>
            
            <h1>Production CI/CD Pipeline</h1>
            <p class="subtitle">
                Application conteneurisée et déployée automatiquement via un pipeline DevOps complet intégrant tests automatisés, analyse de sécurité Trivy, contrôle qualité SonarCloud, AWS ECR et Kubernetes.
            </p>

            <div class="grid">
                <div class="stat-box">
                    <div class="stat-title">Ingénieur DevOps</div>
                    <div class="stat-value">Abdelali Kholty</div>
                </div>
                <div class="stat-box">
                    <div class="stat-title">Orchestrateur</div>
                    <div class="stat-value">AWS EKS (K8s)</div>
                </div>
                <div class="stat-box">
                    <div class="stat-title">Pod Hôte</div>
                    <div class="stat-value">{{ hostname }}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-title">Statut</div>
                    <div class="stat-value" style="color: var(--success);">100% Healthy</div>
                </div>
            </div>

            <div class="tags">
                <span class="tag">🚀 GitHub Actions</span>
                <span class="tag">🛡️ Aqua Trivy</span>
                <span class="tag">📊 SonarCloud SAST</span>
                <span class="tag">📦 Docker & AWS ECR</span>
                <span class="tag">☸️ Kubernetes & AWS EKS</span>
            </div>

            <div class="actions">
                <a href="/health" class="btn btn-primary" target="_blank">🔍 Vérifier le Health Check</a>
                <a href="/profil" class="btn btn-secondary" target="_blank">👤 Consulter le Profil</a>
                <a href="/api/info" class="btn btn-secondary" target="_blank">⚡ Infos Système Pod</a>
            </div>
        </div>

        <footer>
            Conçu & Déployé par Abdelali Kholty &bull; Production CI/CD Pipeline &bull; {{ current_year }}
        </footer>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    hostname = socket.gethostname()
    current_year = datetime.datetime.now().year
    return render_template_string(HTML_TEMPLATE, hostname=hostname, current_year=current_year)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'code': 200,
        'service': 'hello-k8s',
        'pod': socket.gethostname(),
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z'
    })

@app.route('/profil')
def profil():
    return jsonify({
        'nom': 'Kholty',
        'prenom': 'Abdelali',
        'role': 'DevOps & Cloud Engineer',
        'projet': 'Production-Grade CI/CD Pipeline with AWS EKS'
    })

@app.route('/api/info')
def api_info():
    return jsonify({
        'application': 'hello-k8s',
        'framework': 'Flask 3.x',
        'python_version': os.sys.version,
        'pod_name': socket.gethostname(),
        'cluster': 'hello-k8s-cluster (AWS EKS)',
        'region': os.environ.get('AWS_REGION', 'eu-north-1')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
