Perfeito, Danilo. 👨‍💻 Como você decidiu usar os serviços AWS reais — Cognito + API Gateway + Lambda — o projeto lanchonete-auth agora será uma solução 100% alinhada com a arquitetura serverless moderna, e em conformidade com os requisitos da Fase 3 do Tech Challenge.

Aqui está um plano de ação estruturado por etapas, com foco em:
✅ Funcionalidade | 🔐 Segurança | ⚙️ CI/CD | ☁️ Infraestrutura | 📝 Entrega final

⸻

✅ PLANO DE AÇÃO – lanchonete-auth

⸻

🧱 1. Infraestrutura AWS (via SAM/Terraform)

Tarefa	Descrição	Status
1.1	Criar o User Pool no Cognito com CPF como identificador (username ou atributo customizado)	⏳
1.2	Configurar o API Gateway REST com rota /auth (POST) que invoca a Lambda	⏳
1.3	Definir a função Lambda com permissões para consultar usuários no Cognito	⏳
1.4	Definir variáveis de ambiente via template.yaml ou samconfig.toml	⏳
1.5	Adicionar Outputs no template.yaml para facilitar debug e deploy	⏳


⸻

🧠 2. Lógica da Lambda (Autenticação por CPF)

Tarefa	Descrição	Status
2.1	Refatorar autenticacao.py para chamar o Cognito via boto3.client('cognito-idp')	⏳
2.2	Validar CPF (manter validar_cpf.py como está)	✅
2.3	Verificar existência do usuário pelo CPF e, se encontrado, retornar token (JWT ou payload simplificado)	⏳
2.4	(Opcional) Se não encontrado, permitir criação automática no Cognito	⏳
2.5	Adicionar tratativas de erro seguras (usuário inexistente, erro do Cognito etc.)	⏳


⸻

🔐 3. Segurança

Tarefa	Descrição	Status
3.1	Criar segredo do JWT (se local) ou utilizar token do Cognito (caso InitiateAuth)	⏳
3.2	Evitar hardcode de segredos — usar AWS Secrets Manager ou variáveis via Lambda	⏳
3.3	Garantir que apenas o API Gateway acesse a Lambda (via políticas ou configuração SAM)	⏳


⸻

⚙️ 4. CI/CD com GitHub Actions

Tarefa	Descrição	Status
4.1	Criar .github/workflows/deploy.yml com etapas: checkout, sam build, sam deploy	⏳
4.2	Usar OIDC com AWS IAM Role ou AWS_ACCESS_KEY via Secrets	⏳
4.3	Validar que o deploy só ocorra via Pull Requests (proteger a branch main)	⏳


⸻

📦 5. Extras obrigatórios para o Tech Challenge

Tarefa	Descrição	Status
5.1	README.md completo com instruções de deploy, descrição da arquitetura, exemplo de payload	⏳
5.2	samconfig.toml para facilitar o build/deploy padronizado	⏳
5.3	Gravação do vídeo no final, mostrando: arquitetura + checks verdes + execução real	⏳


⸻

🛠️ Extras técnicos recomendados

Tarefa	Descrição	Status
6.1	Criar utils/token.py apenas se não usar Cognito para gerar JWTs	⚠️
6.2	Incluir testes locais com sam local invoke ou script test_local.py	⏳


⸻

📋 Resumo em formato checklist prático

Etapas técnicas:
	•	Criar Cognito (User Pool com CPF)
	•	Integrar Lambda → Cognito com boto3
	•	Refatorar handler (autenticacao.py)
	•	Corrigir template.yaml (Handler, Method POST, Env vars)
	•	Adicionar Outputs e samconfig.toml
	•	Criar workflow CI/CD com GitHub Actions
	•	Configurar secrets/OIDC
	•	Documentar tudo no README.md

Etapas finais:
	•	Validar branch protegida + PR
	•	Gravar vídeo (explicação + execução)
	•	Publicar repositório com acesso ao soat-architecture

⸻

🎯 Quer que eu siga agora com:
	•	Gerar o template.yaml completo (com Cognito + Lambda + API Gateway)?
	•	Criar o esqueleto do CI/CD (.github/workflows/deploy.yml)?
	•	Refatorar o autenticacao.py para usar boto3 com Cognito?

Você escolhe o próximo passo e eu executo. 💡📦