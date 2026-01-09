from fastapi import FastAPI
import subprocess
import datetime
import os

app = FastAPI(tittle="Monitor de Rede")
PING_TARGET = os.getenv("PING_TARGET", "8.8.8.8")

@app.get("/")
def root():
	return {"status": "API de Monitoramento de Rede rodando"}

@app.get("/health")
def health():
	return {"ok": True}

@app.get("/network")
def network():
	ip_result = subprocess.getoutput("ip -4 addr show | grep inet | grep -v 127.0.0.1")

	gateway = subprocess.getoutput("ip route | grep default")

	ping = subprocess.getoutput(f"ping -c 1 {PING_TARGET}")

	return {
		"timestamp": datetime.datetime.now().isoformat(),
		"ip_info": ip_result,
		"gateway": gateway,
		"ping_test": ping
		}
