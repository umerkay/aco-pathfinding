
# Umer Cheatsheet

---

## 🔐 SSH

- SSH to `vyro-vm-port` (host set in config):
  ```bash
  ssh vyro-vm-port
  ```

- SSH with port forwarding (local 7860 → remote 7860):
  ```bash
  ssh -L 7860:localhost:7860 vyro-vm-port
  ```

- SSH with keep-alive + port forwarding:
  ```bash
  ssh -o ServerAliveInterval=30 -o ServerAliveCountMax=5 -L 7860:localhost:7860 vyro-vm-port
  ```

---

## 🎛️ ComfyUI (Run on GPU 0)

```bash
tmux new -s comfyui
cd ~/ComfyUI
conda activate comfyui
CUDA_VISIBLE_DEVICES=0 python main.py --listen 0.0.0.0 --port 8188
```

Access at: `http://localhost:8188`

---

## 🏋️‍♂️ Fluxgym (Training App)

```bash
tmux new -s fluxgym
cd ~/fluxgym
export CUDA_VISIBLE_DEVICES=0
source env/bin/activate
python app.py
```

---

## 🧪 AI Toolkit (LoRA Training)

```bash
tmux new -s aitoolkit
cd ~/ai-toolkit
conda activate ai-toolkit
CUDA_VISIBLE_DEVICES=1 python run.py config/examples/train_lora_flux_24gb_three.yaml
```

---

## 🛠️ Utils

- Check GPU usage:
  ```bash
  nvidia-smi
  ```

- Live GPU watch:
  ```bash
  watch -n 1 nvidia-smi
  ```

- Kill a process by PID:
  ```bash
  kill -9 <pid>
  ```

- Find who started a process (user, location, time):
  ```bash
  ps -fp <pid>
  ```

---

## 🌀 tmux Essentials

- List sessions:
  ```bash
  tmux ls
  ```

- Attach to a session:
  ```bash
  tmux attach -t <session_name>
  ```

- Detach (inside tmux):
  ```
  Ctrl + B, then D
  ```

- Kill a session:
  ```bash
  tmux kill-session -t <session_name>
  ```

---

## 🧬 Conda Environment

- Create a new env:
  ```bash
  conda create -n <env_name> python=3.10
  ```

- Activate env:
  ```bash
  conda activate <env_name>
  ```

- Deactivate env:
  ```bash
  conda deactivate
  ```

- List envs:
  ```bash
  conda env list
  ```

---

## 🐙 Git

- Clone a repo:
  ```bash
  git clone <repo_url>
  ```

- Check status:
  ```bash
  git status
  ```

- Add & commit:
  ```bash
  git add .
  git commit -m "message"
  ```

- Push to origin:
  ```bash
  git push origin main
  ```

- Pull latest:
  ```bash
  git pull
  ```

---

## 🐳 Docker

- Build image:
  ```bash
  docker build -t myimage .
  ```

- Run container:
  ```bash
  docker run -it --gpus all --name mycontainer myimage
  ```

- List containers:
  ```bash
  docker ps -a
  ```

- Start/stop container:
  ```bash
  docker start mycontainer
  docker stop mycontainer
  ```

- Remove container/image:
  ```bash
  docker rm mycontainer
  docker rmi myimage
  ```

