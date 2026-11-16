# Plano de Gerência de Configuração de Software (GCS)

**Projeto:** Simulador Bitcoin
**Autor / Gerente de configuração:** André Felipe dos Santos Ricardo
**Disciplina:** Gerência, Configuração e Processos de Software — Católica SC
**Versão do plano:** 1.0 — 09/11/2026

## 1. Objetivo e escopo
Definir como os itens de configuração do projeto **Simulador Bitcoin** (simulador didático de halving e Proof-of-Work em Python/Streamlit) são identificados, versionados, alterados, revisados, verificados e publicados. Este plano é, ele próprio, um item de configuração e fica versionado em `docs/gcs/plano-gcs.md`.

## 2. Papéis
| Papel | Responsável | Responsabilidades |
| :--- | :--- | :--- |
| Autor / Gerente de configuração / Aprovador de produção | André Felipe (`@itsandrezl`) | Mantém o plano, abre PRs, aprova deploy em `production` |
| Par de revisão | `@SEU-PAR` (acesso de escrita) | Revisa e aprova PRs; atua como comitê de controle de mudanças (CCB) simplificado |

## 3. Identificação dos itens de configuração
| ID | Item | Local | Tipo |
| :--- | :--- | :--- | :--- |
| IC-01 | Código-fonte do simulador | `src/app.py` | Código |
| IC-02 | Testes automatizados | `tests/` | Teste |
| IC-03 | Dependências | `requirements.txt`, `requirements-dev.txt` | Configuração |
| IC-04 | Pipelines de CI/CD | `.github/workflows/` | Automação |
| IC-05 | Plano de GCS | `docs/gcs/plano-gcs.md` | Documento |
| IC-06 | Evidências de conformidade | `docs/gcs/evidencias/` | Documento |
| IC-07 | README e licença | `README.md`, `LICENSE` | Documento |
| IC-08 | Regras de contribuição e templates | `CONTRIBUTING.md`, `.github/` | Processo |

**Convenção de commits:** Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`, `ci:`).
**Convenção de branches:** `feature/<descrição>`, `fix/<descrição>`, `docs/<descrição>`.

## 4. Estrutura do repositório
```
simulador-bitcoin/
├── .github/
│   ├── workflows/        # ci.yml, deploy.yml
│   ├── ISSUE_TEMPLATE/   # solicitação de mudança
│   ├── CODEOWNERS
│   └── pull_request_template.md
├── docs/gcs/
│   ├── plano-gcs.md
│   ├── configuracao-github.md
│   └── evidencias/
├── src/app.py
├── tests/test_app.py
├── requirements.txt
├── requirements-dev.txt
├── CONTRIBUTING.md
├── README.md
└── LICENSE
```

## 5. Estratégia de branches
- `main`: linha estável, equivalente a produção. **Protegida**: sem push direto.
- `develop`: integração, alimenta o ambiente `staging`.
- `feature/*`, `fix/*`, `docs/*`: criadas a partir de `develop`, integradas por Pull Request.

Fluxo: `feature/*` → PR → `develop` → PR → `main`.

## 6. Controle de mudanças
1. Registrar a mudança em uma Issue (modelo "Solicitação de mudança").
2. Criar branch a partir de `develop`.
3. Abrir Pull Request usando o template.
4. CI deve passar (pytest).
5. O par de revisão revisa e aprova (mínimo de 1 aprovação, exigida pela proteção de branch).
6. Merge. Conversas do PR precisam estar resolvidas.

## 7. Baselines e versionamento
Versionamento semântico (`MAJOR.MINOR.PATCH`). Cada baseline é uma **tag** na `main` (ex.: `v1.0.0`) com release no GitHub. Baseline inicial: `v1.0.0`, que inclui estrutura do repositório e este plano.

## 8. Ambientes e publicação
| Ambiente | Origem | Aprovação |
| :--- | :--- | :--- |
| `staging` | `develop` e `main` | Automática |
| `production` | `main`, após staging | **Revisor obrigatório: André Felipe (`@itsandrezl`)** |

O deploy atual é simulado no workflow `deploy.yml`; a estrutura de ambientes e aprovação é a real.

## 9. Auditoria e evidências
Auditorias de configuração verificam: (a) proteção da `main` ativa; (b) PRs com revisão do par; (c) ambientes com revisor; (d) plano publicado e atualizado. As evidências ficam em `docs/gcs/evidencias/`:
- recusa de push direto na `main`;
- par de revisão com acesso de escrita;
- configuração dos environments `staging` e `production`.

## 10. Histórico de revisões do plano
| Versão | Data | Descrição | Autor |
| :--- | :--- | :--- | :--- |
| 1.0 | 09/11/2026 | Versão inicial | André Felipe |
