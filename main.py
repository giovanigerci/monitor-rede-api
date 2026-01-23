from fastapi import FastAPI
import subprocess
from datetime import datetime
import os
import logging

app = FastAPI(tittle="Monitor de Rede")
PING_TARGET = os.getenv("PING_TARGET", "8.8.8.8")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

@app.middleware("http")
async def log_requests(request, call_next):
	tempo_inicio = datetime.now()
	response = await call_next(request)
	tempo_final = datetime.now()
	duracao = (tempo_final - tempo_inicio)
	duracao_ms = round (duracao.total_seconds() * 1000, 2)	 #Serve para colocar o tempo em milissegundos e arredondar para duas casas depois da virgula
	logger.info(
		" | Método: %s | recebido da URL: %s | Status da Resposta: %s | Tempo de duração: %sms|",
		request.method,
		request.url.path,
		response.status_code,
		duracao_ms
	)
	return response

def run_command(command: str) -> str:
	result = subprocess.run(
		command,
		shell=True,
		capture_output=True,
		text=True
	)
	return result.stdout.strip()


def get_ip_info():
	output = run_command("ip -4 addr show eth0")

	for line in output.splitlines():
		if "inet" in line:
			parts = line.split()
			ip, mask = parts[1].split("/")
			return {
				"ip": ip,
				"mask": mask
			}
		
	return None


def get_gateway():
	output = run_command("ip route")

	for line in output.splitlines():
		if line.startswith("default"):
			return line.split()[2]
		
	return None

logger = logging.getLogger("ping")
def ping_target():
	logger.info(
		"Iniciando ping para %s",
		PING_TARGET
	)
	output = run_command(f"ping -c 1 {PING_TARGET}")

	if "time=" in output:
		for line in output.splitlines():
			if "time=" in line:
				time_ms = line.split("time=")[1].split(" ")[0]

				logger.info(
					"Ping bem sucedido para %s (%sms)",
					PING_TARGET,
					time_ms
				)

				return {
					"target": PING_TARGET,
					"success": True,
					"time_ms": float(time_ms),
				}
	logger.warning("Ping não efetuado")
	return{
		"target": PING_TARGET,
		"success": False,
		"time_ms": None
	}		


@app.get("/")
def root():
	return {"status": "API de Monitoramento de Rede rodando"}

@app.get("/health")
def health():
	return {"ok": True}

@app.get("/network")
def network():
	return {
		"timestamp": datetime.now().isoformat(),
		"ip_info": get_ip_info(),
		"gateway": get_gateway(),
		"ping": ping_target()
	}
