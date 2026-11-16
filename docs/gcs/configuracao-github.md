# Passo a passo: configurar o GitHub (feito pela interface)

Estas configurações vivem no GitHub, não no código. Faça nesta ordem.

## 1. Repositório acessível
Settings → General → Danger Zone → visibilidade **Public** (ou convide o professor como colaborador, se for privado). Confira abrindo o link em uma aba anônima.

## 2. Par de revisão com acesso de escrita
Settings → Collaborators → **Add people** → usuário do colega → papel **Write**. Anexe print da lista em `evidencias/`.

## 3. Proteção da `main`
Settings → Branches → Add branch ruleset (ou classic rule) para `main`:
- Require a pull request before merging, com **1 aprovação**
- Require status checks to pass → `build-and-test`
- Require conversation resolution
- Block force pushes (e, se disponível, não permita bypass)

## 4. Evidência da recusa do push direto
```bash
git checkout main
git commit --allow-empty -m "teste: push direto na main"
git push origin main
```
O GitHub deve responder com `remote rejected ... protected branch`. Tire print do terminal e salve em `evidencias/`. Depois desfaça: `git reset --hard origin/main`.

## 5. Environments
Settings → Environments:
- **staging**: sem regras.
- **production**: marque **Required reviewers** e adicione `itsandrezl`. Em Deployment branches, restrinja a `main`.

Anexe prints em `evidencias/`.

## 6. Publicar a estrutura
Como a `main` fica protegida, suba esta estrutura por PR: `feature/estrutura-gcs` → `develop` → `main`, com aprovação do par.
