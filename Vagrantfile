Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/precise64"
  config.vm.provider "hyperv"
  config.vm.synced_folder "C:\\projects\\DevOps-Course-Starter\\", "/vagrant"
  config.vm.provision "shell", privileged: false, inline: <<-SHELL
	sudo apt-get update
	# install pyenv prerequisites
	sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
	# install pyenv
	git clone https://github.com/pyenv/pyenv.git ~/.pyenv
	echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
	echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
	echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
	# install python
	CFLAGS=-I/usr/include/openssl
	LDFLAGS=-L/usr/lib64
	pyenv install -v 3.4.3
	pyenv global 3.4.3
	# install poetry
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
  SHELL
end
