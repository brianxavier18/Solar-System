Esse projeto é uma simulação simples do sistema solar feita com Turtle. 

Visão Geral Rápida do Projeto

Este projeto é uma simulação simples do sistema solar, desenvolvida com a biblioteca Turtle do Python. A estrutura do código é modular, organizada em três módulos principais e um arquivo de configuração:
main.py: Orquestra a simulação, carregando configurações, inicializando a tela, o sol e os planetas. Contém o loop principal, as associações de teclas (keybindings) e a geração automática do arquivo config.json.
display.py: Gerencia as funções de configuração da tela (cor, título, tamanho) e a criação do sol, além de desenhar as órbitas dos planetas.
planets.py: Define a classe Planet, que representa cada planeta e suas funcionalidades (movimento, atualização de ângulo, rótulo persistente).
config.json: Armazena todas as configurações da simulação, como tela, escala, planetas, design e rótulos.
solar system.py: Uma versão antiga/backup do código, mantida no workspace, mas não utilizada pelo main.py modular.
A simulação aceita velocidades reais em km/h para os planetas e as converte para o movimento na tela usando uma escala km_per_pixel.Estrutura de Arquivos

Para referência, os arquivos principais do projeto são:
main.py
display.py
planets.py
config.json
c:\Users\xxx\xxx\solar-system\solar system.py (legado)
main.py — Orquestração e Configuração
Pontos Principais
DEFAULT_CONFIG Embutido: Contém valores padrão para a tela (screen), escala (scale.km_per_pixel), rótulos (labels) e a lista de planetas (nome, raio em pixels, cor, speed_kmh). Isso garante que o programa possa ser executado mesmo sem o config.json.
Carregamento e Fusão de Configurações:
A função load_config(path) tenta abrir config.json. Se o arquivo não existir, ele é criado com o DEFAULT_CONFIG formatado em JSON.
O config.json é lido e um "deep-merge" é realizado com a função deep_merge(dst, src). Se ambos os valores forem dicionários, a fusão é recursiva; caso contrário, o valor de src sobrescreve o de dst.
Retorna a configuração mesclada (padrões com valores do arquivo sobrepostos), permitindo editar apenas partes do config.json.
Inicialização da Tela e Elementos:
setup_screen(cfg) (em display.py) é chamado com a configuração mesclada.
main chama create_sun(color=...) passando cfg['screen']['sun_color'].
draw_orbits(screen, cfg.get('planets', [])) desenha as órbitas usando a configuração orbits.
Criação de Planetas: planets = create_planets_from_config(cfg) cria objetos Planet a partir do config.json e de planet_design (forma e tamanho).
Aplicação de Estilos dos Rótulos: O código aplica a cor global cfg['labels']['color'] e a fonte cfg['labels']['font'] a todos os planetas.
Controles e Variáveis de Runtime:
paused (dicionário com chave value) controla a pausa da simulação (toggle com a tecla espaço).
speed_multiplier (dicionário com value) multiplica a velocidade atual (aumenta com + ou = e diminui com -).
Dicionários são usados para permitir alteração interna nas closures das funções ligadas aos keybindings.
Loop Principal

O loop principal da simulação executa as seguintes etapas:
Cálculo de dt: Calcula o tempo decorrido (dt = now - last_time) em segundos desde o frame anterior.
Atualização dos Planetas: Para cada planeta:
Chama p.move(sun) para posicionar o turtle usando o p.angle atual.
Chama p.step(dt_seconds=dt, km_per_pixel=..., speed_multiplier=...) para atualizar p.angle de acordo com o tempo real e a escala definida.
Chama p.label() para posicionar/atualizar o writer persistente do rótulo do planeta.
Atualização da Tela: screen.update() e time.sleep(sleep_time) para controlar a taxa de atualização.
Tratamento de Erros: Protegido por try/except que captura turtle.Terminator quando a janela é fechada, encerrando o programa sem stacktrace.
Resumo do Loop: Cálculo de dt real → atualizar ângulos proporcionalmente a dt → mover turtles na tela → atualizar display → dormir.display.py — Tela, Sol, ÓrbitasFunções Importantes
setup_screen(cfg): Aplica bgcolor, tracer (controla atualizações automáticas), title e setup(width, height) quando fornecidos. Uma observação importante é que screen.setup() pode variar entre implementações de Turtle/Tk, por isso existe um try/except para evitar falhas.
create_sun(color='yellow'): Cria um turtle para o Sol, definindo sua forma, cor, tamanho (shapesize(2)) e penup().
draw_orbits(screen, planets_cfg): Utiliza um turtle drawer oculto para desenhar círculos com raio p['radius']. Usa as configurações orbits.color e orbits.width (se presentes no config.json). As órbitas permanecem visíveis, pois o código atual não chama drawer.clear().
planets.py — Classe Planet (Detalhada)Classe e Responsabilidades
Construtor (__init__):
def __init__(self, name, radius, color, speed_kmh, shape='circle', shapesize=0.5)
radius é em pixels (posição orbital).
color é a cor visível do turtle.
speed_kmh é a velocidade linear orbital em km/h (valor real para conversão).
shape e shapesize vêm de planet_design no config.json.
Inicializa self.angle (radianos, inicialmente 0), self._label_writer (inicialmente None), self._label_color e self._label_font.
move(self, sun):
Calcula as posições cartesianas a partir do ângulo: x = radius * cos(angle) e y = radius * sin(angle).
Posiciona o planeta em relação ao sol: self.goto(sun.xcor() + x, sun.ycor() + y).
step(self, dt_seconds, km_per_pixel, speed_multiplier=1.0):
Converte a velocidade linear (km/h) em incremento angular (radianos) com base no tempo decorrido (dt_seconds) e na escala km_per_pixel.
Passos da Conversão:
Velocidade linear em pixels/h: linear_pixels_per_hour = speed_kmh / km_per_pixel
Velocidade angular em radianos/h: angular_rad_per_hour = linear_pixels_per_hour / radius_pixels
Incremento angular em dt segundos: delta_angle = angular_rad_per_hour * (dt_seconds / 3600.0) * speed_multiplier
Aplicação: self.angle += delta_angle
Observação: Se radius for 0, o método retorna sem atualizar para evitar divisão por zero.
Em KaTeX:
linear_pixels_per_hour = (\dfrac{\text{speed_kmh}}{\text{km_per_pixel}})
angular_rad_per_hour = (\dfrac{\text{linear_pixels_per_hour}}{\text{radius_pixels}})
delta_angle = (\text{angular_rad_per_hour} \times \dfrac{\text{dt_seconds}}{3600} \times \text{speed_multiplier})
label(self) e set_label_style(...):
label() cria o writer persistente se não existir, posiciona-o perto do planeta e escreve o nome usando a cor/fonte armazenadas.
set_label_style(color, font) altera o estilo usado pelo writer persistente.
Motivações
Performance: Usar um writer persistente por planeta evita criar/descartar turtles a cada frame, melhorando o desempenho.
Realismo: Converter velocidades em km/h permite trabalhar com valores reais, ajustando apenas km_per_pixel para uma velocidade visual agradável.
config.json — Chaves Principais

Exemplo de chaves relevantes (resumido):
screen:
bgcolor: Cor de fundo.
tracer: 0 (atualização manual) ou >0.
sleep: Tempo (s) de espera após cada frame.
title, width, height, sun_color.
scale:
km_per_pixel: Quantos km representam 1 pixel na tela.
Valor menor: Planetas se movem mais pixels por segundo (parecem mais rápidos).
Valor maior: Tudo fica mais devagar.
orbits:
show: true/false (se as órbitas serão exibidas).
color, width.
planet_design:
shape: 'circle' ou outra forma (se implementada).
shapesize: Escala visual do planeta.
labels:
color: Cor global para todos os nomes.
font: Lista [family, size, style].
planets: Lista de objetos com name, radius (pixels), color, speed_kmh.
Observação: O programa cria config.json (com DEFAULT_CONFIG) automaticamente se não existir, fornecendo um arquivo inicial editável.Cálculo de Velocidade Detalhado (com Exemplo Numérico)

Suponha a Terra: speed_kmh = 107208, radius_pixels = 100, km_per_pixel = 1000 (exemplo inicial).
linear_pixels_per_hour = 107208 / 1000 = 107.208 pixels / hour
angular_rad_per_hour = 107.208 / 100 = 1.07208 rad / hour
Em 1 segundo: delta_angle = 1.07208 * (1 / 3600) ≈ 0.0002978 rad
Com km_per_pixel = 1 (escala artificial muito pequena), o movimento é exageradamente rápido:
linear_pixels_per_hour = 107208 / 1 = 107208 pixels/h
angular_rad_per_hour = 107208 / 100 = 1072.08 rad/h
Isso resulta em uma alta taxa de graus/hora, visivelmente rápido na tela.
Portanto, ajuste km_per_per_pixel até encontrar uma "velocidade visual" agradável.Controles de Teclado
espaço: Pausa / retoma (toggle).
+ ou =: Aumenta speed_multiplier (multiplica por 1.5).
-: Diminui speed_multiplier (divide por 1.5).
O multiplicador atua como um acelerador global para simular um avanço rápido.Tratamento de Erros / Casos Limites
Fechar a janela Turtle normalmente lança turtle.Terminator, que é capturado no loop principal para encerrar sem stacktrace.
km_per_pixel nunca deve ser 0 (o código usa max(km_per_pixel, 1e-9) para evitar divisão por zero, mas valores muito pequenos podem resultar em velocidades ridiculamente altas).
radius 0 faz com que o método step retorne sem alterar (evita divisão por zero).
screen.setup(width, height) está em try/except porque nem todas as implementações de Turtle suportam.
Performance e Pontos para Melhorar
Rótulos: Agora são writers persistentes, o que é bom. Anteriormente, um writer era criado por frame, resultando em pior desempenho.
Objetos Turtle: Ainda pode haver muitos objetos Turtle (1 por planeta + writers + drawers). Para cenários com dezenas/centenas de objetos, considere desenho direto em canvas ou uso de imagens estáticas com movimento sem múltiplos turtles.
Atualização de Rótulos: A atualização a cada frame é simples, mas a frequência pode ser reduzida (ex.: a cada N frames) para economizar CPU.
Tracer(0) e update() manual: São bons para performance. Mantenha sleep pequeno o suficiente para suavidade, mas grande o bastante para não sobrecarregar a CPU.
Segurança / Considerações Práticas
config.json é escrito automaticamente na primeira execução. Se o usuário preferir não criar arquivos, pode modificar main.py para desabilitar a escrita.
Não há operações de rede nem manipulação de segredos, garantindo segurança localmente.
Como Executar

No PowerShell, na pasta do projeto:
Na primeira execução, se config.json não existir, o programa criará um com os valores padrão. Edite o arquivo para ajustar os parâmetros e execute novamente.
Debug Rápido (se os planetas não se movem)
Verifique config.json['scale']['km_per_pixel']. Se for muito grande (ex.: 1000, 10000) com velocidades em km/h, o movimento em pixels/segundo pode ser quase zero. Reduza para algo como 1, 10, 100 até ficar visualmente satisfatório.
Certifique-se de que os planetas têm speed_kmh > 0.
Abra a janela e verifique se paused foi acidentalmente ativado (pressione espaço).
Confirme que sleep não é um valor muito alto em screen.sleep.
Execute o snippet de teste (anteriormente fornecido) para inspecionar delta_angle por segundo.
Melhorias Sugeridas (Priorizadas)
Ajustar o padrão razoável para km_per_pixel (ex.: 100) para que, com velocidades reais, a simulação comece com movimento perceptível.
Adicionar um HUD (Head-Up Display) que mostre speed_multiplier, km_per_pixel e o estado paused.
Implementar zoom interativo (+/- para km_per_pixel) com feedback no título.
Permitir posição inicial aleatória ou a partir de elementos reais (ângulos baseados em dados reais).
Trocar formas por imagens (sprites) para um visual melhor.
Escrever testes unitários simples (por exemplo: função de conversão linear → angular).
Mapeamento Rápido: Requisitos do Projeto vs. Implementação Atual
Configurações centralizadas: Implementado (DEFAULT_CONFIG + config.json + deep merge).
Velocidades em km/h: Implementado (speed_kmh e conversão em step).
Rótulos configuráveis: Implementado (cores e fontes globais aplicadas a todos).
Órbitas visíveis: Implementado (via draw_orbits e orbits.show e orbits.color).
Pausar/controle de velocidade: Implementado (espaço / + / -).
Geração automática de config.json: Implementado (primeira execução cria o arquivo).
em três módulos principais + um arquivo de configuração:

main.py — orquestra a simulação: carrega config, inicializa tela/sol/planetas, loop principal, keybindings e geração automática de config.json.
display.py — funções para configurar a tela (cor, título, tamanho) e criar o sol; também desenha as órbitas.
planets.py — classe Planet que representa cada planeta (mover, atualizar ângulo, label persistente).
config.json — configurações (tela, escala, planetas, design, labels, etc).
solar system.py — versão antiga/backup do código (mantida no workspace), não usada pelo main.py modular.
A simulação aceita velocidades reais (km/h) para os planetas e converte isso para movimento na tela usando uma escala km_per_pixel.

Estrutura de arquivos (onde olhar)
main.py
display.py
planets.py
config.json
c:\Users\xavie\Downloads\solar-system\solar system.py (legado)
main.py — orquestração e configuração
Pontos principais:

DEFAULT_CONFIG embutido

DEFAULT_CONFIG contém valores padrão para tela (screen), escala (scale.km_per_pixel), labels, e a lista de planetas (nome, raio em pixels, cor, speed_kmh).
Ter defaults embutidos garante que o programa rode mesmo sem config.json.
Carregamento e merge de configuração

A função load_config(path) faz:
tenta abrir config.json. Se não existir, cria um arquivo com DEFAULT_CONFIG (escreve JSON formatado) — comportamento solicitado.
lê config.json e faz um deep-merge (função deep_merge(dst, src)) onde:
se ambos valores são dicionários, faz merge recursivo;
senão, src sobrescreve dst.
devolve o merged config (defaults com valores do arquivo sobrepostos).
Isso permite editar somente partes do config.json sem precisar repetir todo o conteúdo.
Inicialização da tela e elementos

setup_screen(cfg) (em display.py) é chamado com o cfg mesclado. O main chama create_sun(color=...) passando cfg['screen']['sun_color'] (se houver).
draw_orbits(screen, cfg.get('planets', [])) desenha as órbitas usando a configuração orbits.
Criação de planetas

planets = create_planets_from_config(cfg) cria objetos Planet a partir do config.json e de planet_design (shape & shapesize).
Aplicação de estilos das labels

Atualmente o código aplica sempre a cor global cfg['labels']['color'] (opção do usuário solicitada) e a fonte cfg['labels']['font'] a todos os planetas (atribuição feita logo após criar a lista de planetas).
Controles e variáveis de runtime

paused (dict com chave value) controla pausa; toggle no pressionar da tecla space.
speed_multiplier (dict com value) multiplica a velocidade atual com + / = e diminui com -.
Usamos dicts ({'value': ...}) para permitir alteração interna nas closures das funções ligadas a keybindings.
Loop principal

Calcula dt = now - last_time (segundos passados desde o frame anterior).
Para cada planeta:
chama p.move(sun) que usa o p.angle atual para posicionar o turtle.
chama p.step(dt_seconds=dt, km_per_pixel=..., speed_multiplier=...) — atualiza p.angle de acordo com o tempo real passado e com a escala definida.
chama p.label() para posicionar/atualizar o writer persistente do label do planeta.
screen.update() e então time.sleep(sleep_time) para controlar taxa de atualização.
Protegido por try/except que captura turtle.Terminator quando a janela é fechada.
Resumo do loop:

cálculo de dt real → atualizar ângulos proporcionalmente a dt → mover turtles na tela → atualizar display → dormir.
display.py — tela, sol, órbitas
Funções importantes:

setup_screen(cfg):

Aplica bgcolor, tracer (controla se atualizações são automáticas), title, setup(width, height) quando fornecidos.
Observação: screen.setup() pode variar entre implementações de Turtle/Tk; existe try/except para evitar crash.
create_sun(color='yellow'):

Cria um turtle para o Sol, define shape, color, shapesize(2) e penup().
draw_orbits(screen, planets_cfg):

Usa um turtle drawer oculto para desenhar círculos de raio p['radius'].
Usa configurações orbits.color e orbits.width (quando presente no config.json).
O código atual deixa as órbitas visíveis (não chama drawer.clear()), então elas persistem no canvas.
planets.py — classe Planet (detalhada)
Classe e responsabilidades:

Construtor:

def __init__(self, name, radius, color, speed_kmh, shape='circle', shapesize=0.5):
radius aqui é em pixels (posição orbital do planeta).
color é a cor do turtle (visível).
speed_kmh é a velocidade linear orbital em km/h (valor real usado para conversão).
Shape e shapesize vêm de planet_design no config.
O construtor também inicializa:
self.angle (radianos) — ângulo orbital atual; inicialmente 0.
self._label_writer (inicialmente None) — writer persistente para o label.
self._label_color e self._label_font (estilo local até ser sobrescrito via set_label_style).
move(self, sun):

Calcula posição cartesianas a partir de ângulo:
x = radius * cos(angle)
y = radius * sin(angle)
Faz self.goto(sun.xcor() + x, sun.ycor() + y) — posiciona em relação à posição do sol (que normalmente é 0,0).
step(self, dt_seconds, km_per_pixel, speed_multiplier=1.0):

Este método converte a velocidade linear (km/h) em incremento angular (radianos) dependendo do tempo decorrido no frame dt_seconds e da escala km_per_pixel.
Passos da conversão (implementados no código):
converter velocidade linear de km/h para pixels/h:
linear_pixels_per_hour = speed_kmh / km_per_pixel
obter velocidade angular (radianos por hora):
angular_rad_per_hour = linear_pixels_per_hour / radius_pixels
converter para incremento em dt (segundos):
delta_angle = angular_rad_per_hour * (dt_seconds / 3600.0) * speed_multiplier
aplica: self.angle += delta_angle
Observação: se radius for 0 (evita divisão por zero), o método retorna sem atualizar.
Em KaTeX:

linear_pixels_per_hour = (\dfrac{\text{speed_kmh}}{\text{km_per_pixel}})
angular_rad_per_hour = (\dfrac{\text{linear_pixels_per_hour}}{\text{radius_pixels}})
delta_angle = (\text{angular_rad_per_hour} \times \dfrac{\text{dt_seconds}}{3600} \times \text{speed_multiplier})
label(self) e set_label_style(...)

label() cria o writer persistente se não existir, posiciona-o perto do planeta e escreve o nome usando a cor/fonte armazenadas.
set_label_style(color, font) altera estilo usado pelo writer persistente.
Motivações:

Usar writer persistente por planeta evita criar/descartar turtles a cada frame (melhora performance).
Converter velocidades em km/h permite trabalhar com valores reais e só ajustar km_per_pixel para obter uma velocidade visual agradável.
config.json — chaves principais e como agir sobre elas
Exemplo de chaves relevantes (resumido):

screen:

bgcolor: cor de fundo
tracer: 0 (atualização manual) ou >0
sleep: tempo (s) de espera após cada frame
title, width, height, sun_color
scale:

km_per_pixel: quantos km representam 1 pixel na tela
Valor menor → planetas se movem mais pixels por segundo (parecem mais rápidos)
Valor maior → tudo fica mais devagar.
orbits:

show: true/false (se usar ou não)
color, width
planet_design:

shape: 'circle' ou outro (se implementar)
shapesize: escala visual do planeta
labels:

color: cor global usada para todos os nomes (aplicado globalmente)
font: lista [family, size, style]
planets: lista de objetos com:

name, radius (pixels), color, speed_kmh
Observação: o programa cria config.json (com DEFAULT_CONFIG) se não existir — então você terá um arquivo inicial editável.

Cálculo de velocidade detalhado (com exemplo numérico)
Suponha Earth: speed_kmh = 107208, radius_pixels = 100, km_per_pixel = 1000 (exemplo inicial).

linear_pixels_per_hour = 107208 / 1000 = 107.208 pixels / hour
angular_rad_per_hour = 107.208 / 100 = 1.07208 rad / hour
em 1 segundo: delta_angle = 1.07208 * (1 / 3600) ≈ 0.0002978 rad (corresponde ao que o snippet de teste mostrou)
Com km_per_pixel = 1 (escala artificial muito pequena), o movimento é exageradamente rápido:

linear_pixels_per_hour = 107208 / 1 = 107208 pixels/h
angular_rad_per_hour = 107208 / 100 = 1072.08 rad/h
→ deg/h muito alto (visivelmente rápido na tela).
Portanto ajuste km_per_pixel até encontrar “velocidade visual” agradável.

Controles de teclado
space: pausa / resume (toggle)
ou = : aumentar speed_multiplier (multiplica por 1.5)
: diminuir speed_multiplier (divide por 1.5)
O multiplicador atua como um acelerador global para simular fast-forward.

Tratamento de erros / casos limites
Fechar a janela Turtle normalmente lança turtle.Terminator, capturado no loop principal para encerrar sem stacktrace.
km_per_pixel nunca deve ser 0 (o código usa max(km_per_pixel, 1e-9) para evitar divisão por zero, mas se for muito pequeno você terá velocidades ridiculamente altas).
radius 0 → step retorna sem alterar (evita div/0).
screen.setup(width, height) está em try/except porque nem todas as impl. de Turtle suportam.
Performance e pontos para melhorar
Labels: agora são writers persistentes (bom). Antes criávamos um writer por frame — pior performance.
Ainda pode haver muitos objetos Turtle (1 por planeta + writers + drawers). Para cenários com dezenas/centenas de objetos, considerar desenho direto em canvas ou usar imagens estáticas + movimento sem múltiplos turtles.
Atualizar labels a cada frame é simples; pode reduzir frequência (ex.: a cada N frames) para economizar CPU.
Usar Tracer(0) e update() manual é bom para performance; manter sleep pequeno o suficiente para suavidade, grande o bastante para não matar CPU.
Segurança / considerações práticas
config.json é escrito automaticamente na primeira execução. Se o usuário preferir não criar arquivos, pode modificar main.py para não escrever.
Não há operações de rede nem manipulação de secrets — seguro localmente.
Como executar
No PowerShell, na pasta do projeto:

Na primeira execução, se config.json não existir, o programa irá criar um config.json com os defaults. Edite o arquivo para ajustar parâmetros e rode novamente.

Debug rápido (se planetas não se movem)
Verifique config.json['scale']['km_per_pixel']. Se for muito grande (ex.: 1000, 10000) com speeds em km/h, o movimento em pixels/segundo pode ser praticamente zero. Reduza para algo como 1, 10, 100 até ficar visualmente satisfatório.
Certifique-se que planets têm speed_kmh > 0.
Abra a janela e verifique se paused foi acidentalmente ativado (pressione space).
Confirme que sleep não é enorme no screen.sleep.
Execute o snippet de teste (o que eu rodei anteriormente) para inspecionar delta_angle por segundo.
Melhorias sugeridas (priorizadas)
Ajuste padrão razoável para km_per_pixel (ex.: 100) para que, com speeds reais, a simulação comece com movimento percebível.
Adicionar HUD com velocidade real (km/h) e estado (paused, speed x).
Permitir zoom com teclas (aumentar/diminuir km_per_pixel interativamente).
Permitir posição inicial aleatória ou a partir de elementos reais (ângulos baseados em dados reais).
Trocar shapes por imagens (sprites) para melhor visual.
Escrever testes unitários simples (por exemplo: função de conversão linear → angular).
Mapeamento rápido: requisitos do projeto vs. implementação atual
Configurações centralizadas: implementado (DEFAULT_CONFIG + config.json + deep merge).
Velocidades em km/h: implementado (speed_kmh e conversão em step).
Rótulos configuráveis: implementado (global labels.color e font aplicados a todos).
Órbitas visíveis: implementado (via draw_orbits e orbits.show e orbits.color).
Pausar/controle de velocidade: implementado (space / + / -).
Geração automática de config.json: implementado (primeira execução cria o arquivo).


Atualização:
# Documentação do módulo `star`

Este documento descreve o módulo `star.py` (localizado na raiz do projeto) que gera e atualiza "estrelas" decorativas no plano de fundo da simulação do sistema solar.

## Visão geral

O módulo fornece um sistema simples de partículas visuais (cada "estrela" é uma Turtle) que:
- Surgem aleatoriamente por toda a tela (horizontal e vertical).
- Têm vida curta e fazem um pequeno "piscar" (efeito de fade triangular via `shapesize`).
- Possuem cor individual (tons pastel e/ou cores vivas) que é escolhida quando a estrela é criada.

O objetivo é um efeito estético leve, sem interferir nas órbitas dos planetas.

## Funções públicas

### init_stars(cfg, screen, sun, planet_radii)

- Descrição: cria e retorna uma lista inicial de estrelas. Cada estrela é um dicionário com as chaves: `t` (turtle), `born` (timestamp), `life` (segundos) e `color` (hex string).
- Assinatura: `init_stars(cfg: dict, screen, sun, planet_radii: list) -> list`
- Parâmetros:
  - `cfg`: dicionário carregado de `config.json`. O módulo lê opcionalmente `cfg['stars']` para parâmetros (ver "Configuração" abaixo).
  - `screen`: objeto `turtle.Screen()` utilizado para consulta do canvas (tamanho real) e integração visual.
  - `sun`: turtle do Sol; usada apenas para referência (coordenadas centro).
  - `planet_radii`: lista de raios (pixels) dos planetas — atualmente `init_stars` posiciona estrelas por todo o canvas (não bloqueia totalmente as órbitas), mas os raios podem ser usados em versões futuras.
- Retorno: lista de dicionários representando estrelas.

### update_stars(stars, cfg, now)

- Descrição: atualiza o estado das estrelas existentes (reduz a "vida", aplica shapesize para o efeito de fade, remove as expiradas) e, com probabilidade, cria novas estrelas distribuídas por todo o canvas.
- Assinatura: `update_stars(stars: list, cfg: dict, now: float) -> None`
- Parâmetros:
  - `stars`: lista retornada por `init_stars` (modificada in-place).
  - `cfg`: dicionário de configuração; o módulo pode esperar `cfg['__screen_obj__'] = screen` antes de chamar para usar o tamanho real do canvas.
  - `now`: timestamp atual (ex.: `time.time()`), usado para calcular idade das estrelas.
- Retorno: nada (a lista `stars` é atualizada in-place).

### random_light_color() / random_vivid_color()

- Funções utilitárias que geram strings hex (`#rrggbb`) para cores pastel e cores vivas. Usadas internamente para compor a paleta padrão.

## Estrutura de uma estrela (exemplo)

Cada elemento da lista `stars` tem o formato aproximado:

{
  't': <turtle.Turtle object>,
  'born': 169...,          # timestamp (float)
  'life': 0.5,             # tempo de vida em segundos
  'color': '#f2f7ff'       # cor hexadecimal
}

A `turtle` está posicionada na tela e visível; quando a estrela expira, sua turtle é removida/ocultada (mover para fora da tela).

## Configuração via `config.json`

O módulo lê `cfg.get('stars')` para parâmetros opcionais. Exemplo de seção em `config.json`:

"stars": {
  "count": 120,
  "lifetime": 0.5,
  "spawn_chance": 0.2,
  "max_new_per_frame": 6,
  "colors": ["#ffe6a7", "#ffd1dc", "#a7d8ff", "#d1ffa7"]
}

- `count`: quantidade inicial de estrelas (default: 120).
- `lifetime`: vida padrão em segundos (default: 0.5).
- `spawn_chance`: probabilidade por tentativa de spawn por frame (default: 0.2).
- `max_new_per_frame`: número máximo de tentativas de spawn por frame (default: 6).
- `colors`: lista opcional de hex strings; se presente, é usada como paleta fixa (sem gerar aleatoriamente).

Se `stars` não existir no config, o módulo gera uma paleta aleatória (mix de tons pastel e cores vivas) e usa valores padrão para `count`, `lifetime`, etc.

## Integração com `main.py`

No projeto atual `main.py` já integra o módulo de estrelas da seguinte forma:

- Importa: `from star import init_stars, update_stars`
- Inicializa: `stars = init_stars(cfg, screen, sun, [p.radius for p in planets])`
- No loop principal chama: `update_stars(stars, cfg, now)`
- O atalho `f` foi implementado para regenerar estrelas (chama `init_stars` novamente) e o atalho `r` restaura órbitas originais.

Observações:
- Para que `update_stars` detecte o tamanho real do canvas, `main.py` passa `cfg['__screen_obj__'] = screen` antes de chamar `init_stars`/`update_stars` quando faz a regeneração via atalho.

## Exemplos de uso

Inicializar e usar (simplificado):

from star import init_stars, update_stars
import time

cfg = load_config('config.json')
screen = setup_screen(cfg)
sun = create_sun()

stars = init_stars(cfg, screen, sun, planet_radii=[40,80,100])

while True:
    now = time.time()
    update_stars(stars, cfg, now)
    screen.update()
    time.sleep(0.01)

## Performance e boas práticas

- Cada estrela é uma `turtle.Turtle` — criar/destrocar muitas instâncias rapidamente pode degradar a performance. Se notar lentidão, recomenda-se:
  - Implementar um pool de turtles (reutilizar objetos em vez de criar/destrocar).
  - Reduzir `count`, `spawn_chance` ou `max_new_per_frame`.
  - Reduzir a taxa de atualização (`sleep` maior no loop principal).

- Para efeitos sutis, prefira `shapesize` pequeno (0.04–0.12) e paletas suaves.

## Possíveis melhorias futuras

- Pool de turtles para melhor performance.
- Evitar explicitamente áreas próximas às órbitas (usar `_random_point_avoid_orbits` para spawn contínuo).
- Integração com camada de configuração dinâmica (UI) para ajustar densidade/cores em tempo real.
- Tornar `update_stars` capaz de receber explicitamente o objeto `screen` como terceiro parâmetro em vez de colocar em `cfg['__screen_obj__']`.

## Troubleshooting

- Se as estrelas não aparecem:
  - Verifique se `init_stars` foi chamado e que `stars` não está vazio.
  - Confirme que o loop principal chama `update_stars(stars, cfg, time.time())` regularmente.
  - Em alguns backends do Tkinter o `canvas.winfo_width()` retorna 1 até a janela ser renderizada — o módulo tem fallback para `cfg['screen'].width`.

- Se houver lentidão:
  - Diminua `count` e `max_new_per_frame` no `config.json`.

