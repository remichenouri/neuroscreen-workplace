# Contribuer au projet

Merci de votre intérêt pour ce projet ! Voici comment contribuer efficacement.

## 🚀 Quick Start

git clone https://github.com/remichenouri/ubisoft_people_analytics.git
cd ubisoft_people_analytics
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pre-commit install

text

## 🔧 Développement

### Tests
pytest --cov=src

text

### Linting
ruff check . --fix
mypy src

text

### Commits
Utilisez les [Conventional Commits](https://www.conventionalcommits.org/) :
- `feat:` nouvelle fonctionnalité
- `fix:` correction de bug
- `docs:` documentation
- `test:` ajout de tests

## 📋 Checklist PR

- [ ] Tests ajoutés/modifiés passent
- [ ] Code linté (ruff + mypy)
- [ ] Documentation mise à jour
- [ ] CHANGELOG.md mis à jour