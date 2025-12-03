# 🔍 CRITÉRIOS DE AUDITORIA INTELIGENTE RGP

## 📋 **Visão Geral dos 7 Critérios**

O sistema Audit-IA utiliza 7 critérios principais para detectar inconsistências e possíveis fraudes nos registros do RGP, com pesos que variam de 5 a 30 pontos.

---

## 🏆 **1. Benefícios Sociais vs Outra Renda (30 pontos)**

### **Lógica:**
- **Detecta:** Pescadores que recebem benefícios sociais (Bolsa Família, Renda Brasil) mas declaram possuir outra fonte de renda
- **Dados verificados:** `renda_brasil_ou_bolsa_familia` + `st_possui_outra_fonte_renda`
- **Peso:** 30 pontos (maior peso)

### **Justificativa:**
Este é o critério mais grave pois indica potencial fraude em programas sociais - pessoa que declara ser beneficiária de programa de transferência de renda para famílias de baixa renda mas informa possuir outra fonte de renda.

### **Impacto na amostra:**
- 0 ocorrências nos 50 casos analisados
- Sinaliza bom controle dos benefícios

---

## 🎓 **2. Escolaridade vs Faixa de Renda (20 pontos)**

### **Lógica:**
- **Detecta:** Pescadores com alta escolaridade (Ensino Médio ou Superior) que declaram renda muito baixa
- **Dados verificados:** `nivel_escolaridade` + `fonte_renda_faixa_renda`
- **Condição:** Escolaridade em ['ENSINO MEDIO COMPLETO', 'ENSINO MEDIO INCOMPLETO', 'ENSINO SUPERIOR'] E renda 'Menor que R$1.045,00 por mês'

### **Justificativa:**
Incompatibilidade entre qualificação educacional e renda declarada. Pessoas com ensino médio ou superior geralmente têm acesso a oportunidades melhores, tornando suspeita uma renda tão baixa para atividade de pesca.

### **Impacto na amostra:**
- 11 ocorrências (22% dos casos)
- Caso mais comum na análise

---

## 📱 **3. Tecnologia vs Renda (15 pontos)**

### **Lógica:**
- **Detecta:** Pescadores com acesso a tecnologia (internet + celular) e residência própria, mas com renda muito baixa
- **Dados verificados:** `possui_internet` + `possui_celular` + `tipo_residencia` + `fonte_renda_faixa_renda`
- **Condição:** Tem internet E celular E residência própria E renda em ['Menor que R$1.045,00 por mês', 'De R$1.045,00 a R$2.000,00']

### **Justificativa:**
O acesso a serviços de tecnologia custa dinheiro, e possuir residência própria indica maior estabilidade financeira. A combinação com renda muito baixa gera inconsistência socioeconômica.

### **Impacto na amostra:**
- 0 ocorrências
- Poucos casos se enquadram nesta categoria

---

## 🏢 **4. Filiação Institucional (10 pontos)**

### **Lógica:**
- **Detecta:** Pescadores que não são filiados a colônias ou associações de pesca
- **Dados verificados:** `st_filiado_instituicao`
- **Condição:** Não é filiado

### **Justificativa:**
A filiação institucional é obrigatória para muitos benefícios e representa formalização da atividade pesqueira. Não ser filiado pode indicar informalidade ou irregularidade.

### **Impacto na amostra:**
- 11 ocorrências (22% dos casos)
- Empatado com critério de escolaridade

---

## 🐢 **5. Produtos Protegidos (5 pontos)**

### **Lógica:**
- **Detecta:** Pescadores que declaram pescar espécies protegidas
- **Dados verificados:** `produto_quelonio` + `produto_repteis`
- **Condição:** Pesca de Quelônios ou Répteis

### **Justificativa:**
A pesca de espécies protegidas é regulamentada e geralmente proibida. Pescadores que declaram capturar esses animais podem estar em situação irregular ou desconhecer a legislação.

### **Impacto na amostra:**
- 0 ocorrências
- Nenhum caso com produtos protegidos

---

## 📍 **6. Localização vs Área de Pesca (10 pontos)**

### **Lógica:**
- **Detecta:** Inconsistência entre endereço residencial e área de pesca declarada
- **Dados verificados:** `municipio` vs `nome_municipio`
- **Condição:** Municípios diferentes e ambos preenchidos

### **Justificativa:**
Pescadores geralmente atuam próximo de onde residem. Grande distância entre residência e área de pesca pode indicar inconsistência logística ou informação falsa.

### **Impacto na amostra:**
- 4 ocorrências (8% dos casos)
- Casos leves (geralmente diferenças de grafia)

---

## 📅 **7. Idade vs Tempo de Registro (25 pontos)**

### **Lógica:**
- **Detecta:** Inconsistência entre idade e tempo de registro no RGP
- **Dados verificados:** `dt_nascimento` vs `dt_primeiro_rgp`
- **Condição:** Idade estimada < tempo de registro - 5 anos

### **Justificativa:**
É impossível que um pescador tenha RGP há mais tempo que sua própria idade. Indica erro nos dados ou possível fraude no registro.

### **Impacto na amostra:**
- 0 ocorrências
- Critério complexo, muitos dados incompletos

---

## 📊 **Distribuição dos Pesos**

| Critério | Ponto | % Total | Impacto Esperado |
|----------|-------|--------|----------------|
| Benefícios vs Renda | 30 | 30% | 🔴 Alto |
| Idade vs Tempo | 25 | 25% | 🔴 Alto |
| Escolaridade vs Renda | 20 | 20% | 🟠 Médio |
| Tecnologia vs Renda | 15 | 15% | 🟢 Baixo |
| Localização vs Área | 10 | 10% | 🟢 Baixo |
| Filiação Institucional | 10 | 10% | 🟢 Baixo |
| Produtos Protegidos | 5 | 5% | 🟢 Baixo |
| **TOTAL** | **115** | **100%** | - |

---

## 🎯 **Limiares de Classificação**

- **Alto Risco:** Score ≥ 60 pontos
- **Médio Risco:** 30 ≤ Score < 60 pontos
- **Baixo Risco:** Score < 30 pontos

---

## 🤔 **Análise dos Resultados**

### **Impacto Real na Amostra:**
- **0%** casos de alto risco
- **6%** casos de médio risco
- **94%** casos de baixo risco

### **Critérios Mais Ativados:**
1. **Escolaridade vs Renda** (11 casos)
2. **Filiação Institucional** (11 casos)
3. **Localização vs Área** (4 casos)

### **Critérios Nunca Ativados:**
- Benefícios vs Renda (melhor controle social)
- Produtos Protegidos (conscientização ambiental)
- Idade vs Tempo (dados limitados)

---

## 💡 **Sugestões de Melhoria**

### 🔧 **Ajustes de Pesos:**
- Considerar reduzir peso de **Escolaridade vs Renda** (atualmente 20 pontos) - pode ser muito rigoroso
- Aumentar peso de **Filiação Institucional** (atualmente 10 pontos) - é fundamental

### 📈 **Novos Critérios a Considerar:**
1. **Tempo de Atividade vs Quantidade de Embarcações**
2. **Categoria Pescadora vs Tipos de Produto**
3. **Seguro Defeso vs Declarações de Renda**
4. **Consistência entre Data de Nascimento e Documentos**
5. **Análise de Padrões Geográficos (clusterização de dados suspeitos)**

### 🔍 **Melhorias na Análise:**
- Cruzar com outras bases de dados disponíveis
- Implementar machine learning para detecção de padrões
- Adicionar análise de similaridade entre perfis
- Considerar contexto histórico dos registros

---

## 📋 **Parâmetros Configuráveis**

Os pesos podem ser ajustados no arquivo `analise_50_resultados.py` nas linhas 62-103 para refinar a sensibilidade do sistema às características específicas do RGP.