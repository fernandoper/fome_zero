# 1. Problema de Negócio

A empresa Fome Zero é um marketplace de restaurantes cujo objetivo principal é facilitar o encontro e as negociações entre clientes e restaurantes. Na 
plataforma da Fome Zero, os restaurantes podem se cadastrar e compartilhar informações como endereço, tipo de culinária servida, disponibilidade de reservas, 
opções de entrega, avaliações de serviços, entre outros. O CEO busca uma compreensão mais aprofundada sobre o negócio para tomar decisões estratégicas mais informadas 
e, assim, alavancar ainda mais a Fome Zero. Para tal, ele solicitou uma análise detalhada dos dados da empresa e a criação de dashboards para responder a uma série de
perguntas pertinentes relacionadas a restaurantes, países, cidades e tipos de culinária.

## Geral

1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?

## País

1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4
registrados?
4. Qual o nome do país que possui a maior quantidade de tipos de culinária
distintos?
5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem
entrega?
7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam
reservas?
8. Qual o nome do país que possui, na média, a maior quantidade de avaliações
registrada?
9. Qual o nome do país que possui, na média, a maior nota média registrada?
10. Qual o nome do país que possui, na média, a menor nota média registrada?
11. Qual a média de preço de um prato para dois por país?
    
## Cidade

1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de
4?
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de
2.5?
4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária
distintas?
6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
reservas?
7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
entregas?
8. Qual o nome da cidade que possui a maior quantidade de restaurantes que
aceitam pedidos online?

## Restaurantes
1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de uma prato para duas
pessoas?
4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor
média de avaliação?
5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que
possui a maior média de avaliação?
6. Os restaurantes que aceitam pedido online são também, na média, os
restaurantes que mais possuem avaliações registradas?
7. Os restaurantes que fazem reservas são também, na média, os restaurantes que
possuem o maior valor médio de um prato para duas pessoas?
8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América
possuem um valor médio de prato para duas pessoas maior que as churrascarias
americanas (BBQ)?

## Tipos de Culinária
1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a maior média de avaliação?
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a menor média de avaliação?
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a maior média de avaliação?
4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a menor média de avaliação?
5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a maior média de avaliação?
6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a menor média de avaliação?
7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a maior média de avaliação?
8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a menor média de avaliação?
9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a maior média de avaliação?
10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a menor média de avaliação?
11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas
pessoas?
12. Qual o tipo de culinária que possui a maior nota média?
13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos
online e fazem entregas?

# 2. Premissas assumidas para a análise
1. A última atualização do dataset ocorreu em 2019.
2. Foi assumido que o modelo de negócio é um marketplace.
3. A análise contemplou uma amostra de 5900 restaurantes, distribuídos em 15 países.
4. As três principais perspectivas de negócio abordadas foram: Cidades, Países e Culinárias.

# 3. Estratégia da solução
Desenvolvemos um painel estratégico utilizando métricas que refletem as três principais perspectivas do modelo de negócio da empresa:
1. Visão das cidades cadastradas.
2. Visão dos países cadastrados.
3. Visão das culinárias cadastradas.
  
# 4. Top Insights de dados
1. Um grande número de restaurantes possui classificação 0, possivelmente indicando novos estabelecimentos ou aqueles que ainda não alcançaram um padrão mínimo de avaliação.
A maioria dos restaurantes tem uma classificação entre 2,5 e 4,5, mostrando um padrão de alta qualidade.
2. A maioria dos restaurantes tem uma classificação entre 2,5 e 4,5, indicando que muitos restaurantes neste conjunto de dados são bem avaliados.
3. Muito poucos restaurantes têm uma classificação acima de 4,5, tornando-os excepcionais.
4. Cozinhas do Norte da Índia e chinesa dominam em popularidade.
5. Restaurantes com opção de reserva tendem a ter avaliações ligeiramente melhores.

# 5. O produto final do projeto
Desenvolvemos um painel online, hospedado na nuvem e acessível por qualquer dispositivo conectado à internet. O painel pode ser acessado através do link: 
https://fernando-fomezero.streamlit.app/

# 6. Conclusão
Este conjunto de dados oferece uma visão profunda dos restaurantes listados em um popular marketplace. Algumas observações notáveis incluem:
1. **Classificações de Restaurantes**: A maioria dos estabelecimentos possui classificações entre 2,5 e 4,5. No entanto,
   é interessante notar um grande número de restaurantes com classificação 0, o que pode indicar estabelecimentos novos ou
   aqueles que ainda não alcançaram um padrão mínimo de avaliação.
2. **Popularidade de Culinárias**: A culinária do Norte da Índia e a culinária chinesa destacam-se como as mais populares, com outras cozinhas,
   como Fast Food e Mughlai, também marcando presença significativa. Isso sugere uma inclinação para sabores ricos e variados entre os restaurantes deste conjunto de dados.
3. **Reservas e Qualidade**: Os restaurantes que oferecem a opção de reserva de mesa tendem a ser percebidos de forma mais favorável,
   com classificações médias ligeiramente mais altas em comparação com os que não oferecem. Isso pode ser um indicativo da importância de oferecer
   conveniências modernas e serviços adicionais para melhorar a percepção do cliente.
4. Recomenda-se a potenciais investidores, gerentes de restaurante e entusiastas da gastronomia que explorem este conjunto de dados mais a fundo para obter insights adicionais que possam ajudar nas decisões estratégicas e operacionais.

# 7. Próximo passos
1. **Feedback dos Clientes**: Analisar feedback textual dos clientes pode fornecer insights sobre pontos fortes e áreas de melhoria.
2. **Análise Temporal**: Se disponível, analisar tendências ao longo do tempo pode revelar padrões sazonais.
3. **Comparação Regional**: Analisar dados por localização pode revelar preferências regionais.
4. **Impacto do Preço na Classificação**: Entender a relação entre preço e classificação pode ajudar a otimizar a estratégia de preços.
5. **Integração com Dados Externos**: Combinar este dataset com outras fontes pode enriquecer a análise.




















   
