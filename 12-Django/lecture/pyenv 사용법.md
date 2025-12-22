# pyenv & pyenv-virtualenv 사용 방법

---

## 1. pyenv / pyenv-virtualenv 설치

Homebrew를 사용하여 pyenv와 pyenv-virtualenv를 설치한다.

```bash
brew install pyenv
brew install pyenv-virtualenv
```

## 2. 사용 중인 Shell 확인

현재 사용 중인 셸을 확인한다.
이 값에 따라 설정 파일(.zshrc, .bashrc 등)이 달라진다.

```bash
echo $SHELL
```

## 3. pyenv-virtualenv 초기화 설정

~/.zshrc 파일에 pyenv-virtualenv 초기화 코드를 추가한다.
이 설정은 Shell이 시작될 때 pyenv의 가상환경 기능을 사용할 수 있도록 한다.

```bash
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
```

## 4. Shell 설정 적용

변경된 .zshrc 설정을 현재 터미널 세션에 즉시 반영한다.

```bash
source ~/.zshrc
```

## 5. 설치 가능한 Python 인터프리터 목록 확인

pyenv를 통해 설치할 수 있는 Python 인터프리터 버전 목록을 확인한다.

```bash
pyenv install --list
pyenv install -l  # 축약형
```

## 6. Python 인터프리터 설치

목록에서 원하는 Python 버전을 선택하여 설치한다.
이 명령은 Python 인터프리터 실행 파일 자체를 설치한다.

```bash
pyenv install [python version]
pyenv install 3.12.2 # Example
```

## 7. 가상환경(virtualenv) 생성

설치된 특정 Python 인터프리터를 기반으로 가상환경을 생성한다.

```bash
pyenv virtualenv [python version] [virtualenv name]
pyenv virtualenv 3.12.2 my-env # Example
```

## 8. 프로젝트 디렉토리에 가상환경 적용
가상환경을 사용하고자 하는 디렉토리에서 해당 가상환경을 로컬로 설정한다.

```bash
pyenv local [virtualenv name]
pyenv local my-env # Example
```