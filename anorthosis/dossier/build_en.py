"""Genera el dossier en inglés (out/) a partir del dossier en español (src/).
Ejecutar: python3 build_en.py"""
import os, re, json, shutil

H = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = os.path.join(H, 'src'), os.path.join(H, 'out')


class Doc:
    def __init__(self, name):
        self.name = name
        self.t = open(os.path.join(SRC, name), encoding='utf-8').read()

    def R(self, a, b, n=1):
        c = self.t.count(a)
        assert c == n, (self.name, a[:80], c)
        self.t = self.t.replace(a, b)

    def RS(self, pairs):
        for p in pairs:
            self.R(*p)

    def json_var(self, var, fn):
        """Aplica fn al JSON asignado a `const var=`."""
        i = self.t.index('const ' + var + '=') + len('const ' + var + '=')
        obj, end = json.JSONDecoder().raw_decode(self.t, i)
        fn(obj)
        self.t = self.t[:i] + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + self.t[end:]

    def save(self, name=None):
        open(os.path.join(OUT, name or self.name), 'w', encoding='utf-8').write(self.t)


# ======================= index.html (contenedor) =======================
ix = Doc('index.html')
ix.RS([
    ('<title>Dossier Ourense FIBWI Palma</title>', '<title>Hoop Assistant Sample Dossier</title>'),
    ('<nav aria-label="Secciones">', '<nav aria-label="Sections">'),
    ('Dossier <small>FIBWI Palma</small>', 'Dossier <small>Anorthosis Famagusta</small>'),
    ('<a class="lk" href="#propio">Scouting propio</a>', '<a class="lk" href="#propio">Self-scouting</a>'),
    ('<a class="lk" href="#rival">Scouting rival</a>', '<a class="lk" href="#rival">Opponent scouting</a>'),
    ('<a class="lk" href="#jugadores">Jugadores</a>', '<a class="lk" href="#jugadores">Players</a>'),
    ('<div class="kick">Informe de scouting · Octubre 2026</div>', '<div class="kick">Sample scouting report · October 2026</div>'),
    ('<p class="for">Preparado para el cuerpo técnico de <b>FIBWI Palma</b>. Tres bloques: cómo jugamos nosotros, cómo juega el rival y quién es quién en su plantilla.</p>',
     '<p class="for">Prepared for the coaching staff of <b>Anorthosis Famagusta BC</b> as a sample of our work. Three blocks: how our own club plays, how the opponent plays and who is who on their roster.</p>'),
    ('<span class="state ok">Disponible</span><h3>Scouting propio</h3><p>FIBWI Palma ante Movistar Estudiantes (última jornada). Se acumula cada semana.</p>',
     '<span class="state ok">Available</span><h3>Self-scouting</h3><p>Our own club in its last game. The data builds up every week.</p>'),
    ('<span class="state ok">Disponible</span><h3>Scouting rival</h3><p>Ataque y defensa de Ourense, filtrable por partido, set y jugada. Vídeo incluido.</p>',
     '<span class="state ok">Available</span><h3>Opponent scouting</h3><p>Ourense offense and defense, filterable by game, set and play. Video included.</p>'),
    ('<span class="state ok">Disponible · 10 fichas</span><h3>Jugadores</h3><p>Fichas individuales con PDF descargable y vídeo.</p>',
     '<span class="state ok">Available · 10 profiles</span><h3>Players</h3><p>Individual profiles with a downloadable PDF and video.</p>'),
    ('<div class="eyebrow">Bloque 1</div>\n    <h2>Scouting <em>propio</em></h2>', '<div class="eyebrow">Block 1</div>\n    <h2>Self-<em>scouting</em></h2>'),
    ('<p class="lead">Cómo juega FIBWI Palma: qué funciona y qué no. Este análisis parte del último partido, ante Movistar Estudiantes, y los datos se acumulan jornada a jornada.</p>',
     '<p class="lead">How our own club plays: what works and what does not. This analysis starts from the last game, and the data builds up round by round.</p>'),
    ('<div class="eyebrow">Bloque 2</div>\n    <h2>Scouting <em>rival</em></h2>', '<div class="eyebrow">Block 2</div>\n    <h2>Opponent <em>scouting</em></h2>'),
    ('<p class="lead">Cómo ataca y cómo defiende Ourense. Pulsa en cualquier barra del análisis para filtrar el resto de gráficos.</p>',
     '<p class="lead">How Ourense attacks and how they defend. Click any bar in the analysis to filter the rest of the charts.</p>'),
    ('<h3>Vídeo del rival</h3><p>Se abre en YouTube, en otra pestaña.</p>', '<h3>Opponent video</h3><p>Opens on YouTube, in a new tab.</p>'),
    ('Ver en YouTube', 'Watch on YouTube', 2),
    ('<span>Análisis interactivo</span><button class="lnk" type="button" data-fs="fs-rival">Pantalla completa</button>',
     '<span>Interactive analysis</span><button class="lnk" type="button" data-fs="fs-rival">Full screen</button>'),
    ('title="Scouting rival de Ourense"', 'title="Ourense opponent scouting"'),
    ('<div class="eyebrow">Bloque 3</div>\n        <h2>Scouting de <em>jugadores</em></h2>', '<div class="eyebrow">Block 3</div>\n        <h2>Player <em>scouting</em></h2>'),
    ('<p class="lead">Una ficha por jugador de Ourense: rol, tendencias en ataque y defensa, mapa de tiro, tipos de jugada y defensores asignados.</p>',
     '<p class="lead">One profile per Ourense player: role, offensive and defensive tendencies, shot chart, play types and assigned defenders.</p>'),
    ('Descargar PDF</a>', 'Download PDF</a>'),
    ('>Guardar ficha como imagen</button>', '>Save profile as image</button>'),
    ('<button class="btn ghost" id="vfs" type="button">Pantalla completa</button>', '<button class="btn ghost" id="vfs" type="button">Full screen</button>'),
    ('Para guardar una ficha, haz clic derecho sobre la imagen o mantenla pulsada.', 'To save a profile, right-click the image or press and hold it.'),
    ('aria-label="Fichas de jugadores"', 'aria-label="Player profiles"'),
    ('alt="Ficha 1 de 10"', 'alt="Profile 1 of 10"'),
    ('aria-label="Ficha anterior"', 'aria-label="Previous profile"'),
    ('aria-label="Ficha siguiente"', 'aria-label="Next profile"'),
    ('<small>Ficha</small>', '<small>Profile</small>'),
    ('Usa las flechas del teclado o toca las miniaturas.', 'Use the arrow keys or tap the thumbnails.'),
    ('<button class="lnk" id="vclose" type="button">Cerrar</button>', '<button class="lnk" id="vclose" type="button">Close</button>'),
    ('<h3>Vídeo de jugadores</h3><p>Se abre en YouTube, en otra pestaña.</p>', '<h3>Player video</h3><p>Opens on YouTube, in a new tab.</p>'),
    ('<span>Hoop Assistant · Scouting y análisis de vídeo de baloncesto</span><span>Dossier Ourense · Octubre 2026</span>',
     '<span>Hoop Assistant · Basketball scouting and video analysis</span><span>Sample dossier · Ourense · October 2026</span>'),
    # JS
    ("<span>Análisis interactivo</span><button class=\"lnk\" type=\"button\" data-fs=\"fs-propio\">Pantalla completa</button>",
     "<span>Interactive analysis</span><button class=\"lnk\" type=\"button\" data-fs=\"fs-propio\">Full screen</button>"),
    ('title="Scouting propio de FIBWI Palma"', 'title="Self-scouting of our own club"'),
    ("<span class=\"state wait\">En preparación</span><h3>Análisis propio en camino</h3><p>Este bloque se publica aquí en cuanto se cruzan los datos de los partidos de FIBWI Palma.</p>",
     "<span class=\"state wait\">In progress</span><h3>Self-scouting on its way</h3><p>This block is published here as soon as the game data has been cross-referenced.</p>"),
    ("b.setAttribute('aria-label','Ficha '+(i+1));", "b.setAttribute('aria-label','Profile '+(i+1));"),
    ("img.alt='Ficha '+(cur+1)+' de '+N;", "img.alt='Profile '+(cur+1)+' of '+N;"),
    ("say.textContent='Guardado.'", "say.textContent='Saved.'"),
    ("say.textContent='No se pudo guardar desde aquí.'", "say.textContent='Could not save from here.'"),
    ("'FIBWI_Palma_Ficha_'", "'Ourense_Profile_'"),
    ("b.textContent=on?'Cerrar':'Pantalla completa';", "b.textContent=on?'Close':'Full screen';"),
    ("document.getElementById('vfs').textContent=on?'Cerrar':'Pantalla completa';", "document.getElementById('vfs').textContent=on?'Close':'Full screen';"),
])
assert not re.search(r'(?i)palma|fibwi|estudiantes', ix.t), 'index: queda Palma'

# ======================= propio.html (club propio) =======================
pr = Doc('propio.html')
FAM = {'Rebote ofensivo': 'Offensive rebound', 'Transición': 'Transition', 'SLOB (saque de banda)': 'SLOB (sideline)', 'BLOB (saque de fondo)': 'BLOB (baseline)'}
CAT = {'Media pista': 'Half court', 'Rebote ofensivo': 'Offensive rebound', 'SLOB (banda)': 'SLOB (sideline)', 'Transición': 'Transition',
       'Secundario': 'Secondary break', 'Contra presión': 'Vs press', 'BLOB (fondo)': 'BLOB (baseline)'}
OUTP = {'Tiros libres': 'Free throws', 'Pérdida': 'Turnover', 'Canasta de 2': '2PT made', 'Sin anotar': 'No score', 'Canasta de 3': '3PT made', 'Canasta + falta': 'And-one'}
VAR = {'Directo': 'Direct', 'Robo y bandeja': 'Steal and layup', 'Falta en transición': 'Transition foul', '1c1': '1-on-1',
       'Transición ofensiva': 'Offensive transition', 'Transición': 'Transition', 'Flex screen vs presión': 'Flex screen vs press',
       'Ventaja temprana en poste': 'Early post advantage', 'Sin nota': 'No note', 'Middle PNR sin replace, se queda dentro': 'Middle PNR, no replace, stays inside',
       'Middle PNR sin replace': 'Middle PNR, no replace', 'Rebote ofensivo': 'Offensive rebound', 'Transición de 3': '3-man transition',
       'Roll & replace desde baseline': 'Roll & replace from baseline', 'Transición con números': 'Transition with numbers', 'Sin set definido': 'No defined set',
       'Break 1c1': 'Break 1-on-1', 'Break de 3': 'Break 3', 'Side PNR de 2': 'Side PNR of 2', 'Zipper entry vs presión': 'Zipper entry vs press'}
NOTE = {'nada': 'nothing', 'Double DHO Middle PNR roll replace (Zipper entry en todas)': 'Double DHO Middle PNR roll replace (Zipper entry on all)'}
SHOTD = {'Abierto': 'Open', 'Defendido': 'Contested', 'n/d': 'n/a'}


def fix_propio(D):
    for p in D['plays']:
        for k, m in (('fam', FAM), ('fam0', FAM), ('cat', CAT), ('out', OUTP), ('var', VAR), ('var0', VAR), ('note', NOTE)):
            if p.get(k) in m:
                p[k] = m[p[k]]
        if p.get('clock') == 'n/d':
            p['clock'] = 'n/a'
    for s in D['shots']:
        s['d'] = SHOTD.get(s['d'], s['d'])


pr.json_var('D', fix_propio)
pr.RS([
    ('<title>Scouting Propio Fibwi Palma</title>', '<title>Self-Scouting Dashboard</title>'),
    ('alt="Hoop Assistant" width="34" height="34" style="display:block">Hoop Assistant × Fibwi Palma</a>', 'alt="Hoop Assistant" width="34" height="34" style="display:block">Hoop Assistant · Our club</a>'),
    ('<a class="l" href="#saques">Saques</a>', '<a class="l" href="#saques">Inbounds</a>'),
    ('<a class="l" href="#contextos">Tiempo muerto</a><a class="l" href="#quintetos">Quintetos</a><a class="l" href="#tiro">Tiro</a><a class="l" href="#jugadores">Jugadores</a>',
     '<a class="l" href="#contextos">Timeouts</a><a class="l" href="#quintetos">Lineups</a><a class="l" href="#tiro">Shooting</a><a class="l" href="#jugadores">Players</a>'),
    ('aria-label="Cambiar entre tema claro y oscuro">Tema</button>', 'aria-label="Switch between light and dark theme">Theme</button>'),
    ('document.documentElement.lang="es"', 'document.documentElement.lang="en"'),
    ('<p class="eyebrow">Scouting propio · Fibwi Palma vs Movistar Estudiantes · Última jornada · 25/10/2026</p>', '<p class="eyebrow">Self-scouting · Our club · Last game</p>'),
    ('<div class="score"><span>Fibwi Palma</span><b class="lose">78</b><span>Movistar Estudiantes</span><b>94</b></div>',
     '<div class="score"><span>Our club</span><b class="lose">78</b><span>Opponent</span><b>94</b></div>'),
    ('<h1>Vuestro ataque, <em>jugada a jugada.</em></h1>', '<h1>Our offense, <em>play by play.</em></h1>'),
    ('<p class="eyebrow">Vuestros sets</p>\n  <h2>Lo que jugáis <em>y lo que os rinde</em></h2>', '<p class="eyebrow">Our sets</p>\n  <h2>What we run <em>and what it gives us</em></h2>'),
    ('<button type="button" id="expand">Expandir todo</button><button type="button" id="collapse">Contraer todo</button>',
     '<button type="button" id="expand">Expand all</button><button type="button" id="collapse">Collapse all</button>'),
    ('<p class="eyebrow">Datos</p>\n  <h2>Panel de <em>equipo propio</em></h2>', '<p class="eyebrow">Data</p>\n  <h2>Self-scouting <em>dashboard</em></h2>'),
    ('<label>Ver por<select id="dim"></select></label>', '<label>View by<select id="dim"></select></label>'),
    ('<label>Métrica<select id="met"><option value="ppp">PPP</option><option value="n">Jugadas</option><option value="tov">% de pérdidas</option></select></label>',
     '<label>Metric<select id="met"><option value="ppp">PPP</option><option value="n">Plays</option><option value="tov">% turnovers</option></select></label>'),
    ('<label>Orden<select id="ord"><option value="desc">De mayor a menor</option><option value="asc">De menor a mayor</option></select></label>',
     '<label>Order<select id="ord"><option value="desc">High to low</option><option value="asc">Low to high</option></select></label>'),
    ('<label>Mín. jugadas<input', '<label>Min. plays<input'),
    ('<h3 id="cliptitle" style="margin-top:26px">Todas las jugadas</h3>', '<h3 id="cliptitle" style="margin-top:26px">All plays</h3>'),
    ('<th>Min. vídeo</th><th>Cuarto</th><th>Jugada</th><th>Finaliza</th><th>Resultado</th><th class="n">Pts</th>',
     '<th>Video min.</th><th>Quarter</th><th>Play</th><th>Finisher</th><th>Result</th><th class="n">Pts</th>'),
    ('padding:0">Ver más clips</button>', 'padding:0">Show more clips</button>'),
    ('<p class="eyebrow">Saques</p>\n  <h2>Banda <em>y fondo</em></h2>', '<p class="eyebrow">Inbounds</p>\n  <h2>Sideline <em>and baseline</em></h2>'),
    ('<p class="eyebrow">Después de la parada</p>\n  <h2>Tras tiempo muerto <em>e inicio de cuarto</em></h2>', '<p class="eyebrow">After a stoppage</p>\n  <h2>After timeouts <em>and quarter starts</em></h2>'),
    ('<p class="eyebrow">Quintetos · Synergy</p>\n  <h2>Qué cinco <em>rinden mejor</em></h2>', '<p class="eyebrow">Lineups · Synergy</p>\n  <h2>Which five <em>perform best</em></h2>'),
    ('<p class="eyebrow">Tiro</p>\n  <h2>De dónde llegan <em>los puntos</em></h2>', '<p class="eyebrow">Shooting</p>\n  <h2>Where the <em>points come from</em></h2>'),
    ('<p class="eyebrow">Finalizadores</p>\n  <h2>Quién <em>cierra la jugada</em></h2>', '<p class="eyebrow">Finishers</p>\n  <h2>Who <em>finishes the play</em></h2>'),
    ('<footer>Hoop Assistant · Scouting y análisis de vídeo de baloncesto.<br>PPP por posesión (1,05): puntos entre 74 posesiones. PPP en sets, saques y variantes: puntos por jugada; cada clip es una jugada y el rebote ofensivo cuenta como jugada propia. Uso: porcentaje de las 87 jugadas. Un solo partido: con pocas jugadas, leerlo como tendencia.</footer>',
     '<footer>Hoop Assistant · Basketball scouting and video analysis.<br>PPP per possession (1.05): points over 74 possessions. PPP in sets, inbounds and variants: points per play; each clip is one play and an offensive rebound counts as its own play. Usage: share of the 87 plays. A single game: with few plays, read it as a trend.</footer>'),
    # JS
    ("x.toLocaleString('es-ES',", "x.toLocaleString('en-GB',"),
    ("p.brkL=p.brk?'Con break play':'Sin break play';", "p.brkL=p.brk?'With break play':'No break play';"),
    ("p.out==='Pérdida'", "p.out==='Turnover'", 1),
    ("x.out==='Pérdida'", "x.out==='Turnover'", 3),
    ("{'Canasta de 3':'p3','Canasta de 2':'p2','Canasta + falta':'p3','Tiros libres':'ft','Pérdida':'tov','Sin anotar':'zero'}",
     "{'3PT made':'p3','2PT made':'p2','And-one':'p3','Free throws':'ft','Turnover':'tov','No score':'zero'}"),
    ("[[NP,'Posesiones'],[N,'Jugadas'],[f1(TOT/NP),'PPP por posesión'],[m3+'/'+t3.length,'Triples ('+Math.round(100*m3/t3.length)+'%)'],[TOV,'Pérdidas']]",
     "[[NP,'Possessions'],[N,'Plays'],[f1(TOT/NP),'PPP per possession'],[m3+'/'+t3.length,'Threes ('+Math.round(100*m3/t3.length)+'%)'],[TOV,'Turnovers']]"),
    ("/^(SLOB|BLOB|Break play|Rebote ofensivo|Transición)/", "/^(SLOB|BLOB|Break play|Offensive rebound|Transition)/"),
    ("s.d==='Abierto'", "s.d==='Open'"), ("s.d==='Defendido'", "s.d==='Contested'"), ("s.d==='n/d'", "s.d==='n/a'"),
    ("g.k==='SLOB (banda)'", "g.k==='SLOB (sideline)'"), ("g.k==='BLOB (fondo)'", "g.k==='BLOB (baseline)'"),
    ("`Break play es lo más repetido: ${brk.n} de ${N} jugadas, ${f1(brk.ppp)} PPP`", "`Break play is the most repeated: ${brk.n} of ${N} plays, ${f1(brk.ppp)} PPP`"),
    ("`Mejor set: ${SETF[0].k}, ${f1(SETF[0].ppp)} PPP en ${SETF[0].n} jugadas. Peor: ${SETF[SETF.length-1].k}, ${f1(SETF[SETF.length-1].ppp)} PPP en ${SETF[SETF.length-1].n}`",
     "`Best set: ${SETF[0].k}, ${f1(SETF[0].ppp)} PPP in ${SETF[0].n} plays. Worst: ${SETF[SETF.length-1].k}, ${f1(SETF[SETF.length-1].ppp)} PPP in ${SETF[SETF.length-1].n}`"),
    ("`Saques: SLOB ${f1(slobG.ppp)} PPP en ${slobG.n} jugadas, BLOB ${f1(blobG.ppp)} PPP en ${blobG.n}`", "`Inbounds: SLOB ${f1(slobG.ppp)} PPP in ${slobG.n} plays, BLOB ${f1(blobG.ppp)} PPP in ${blobG.n}`"),
    ("`Tras tiempo muerto: ${ppp(atoL)} PPP en ${atoL.length} posesiones. Inicios de partido y de cuarto: ${ppp(opL)} PPP en ${opL.length}`",
     "`After timeouts: ${ppp(atoL)} PPP in ${atoL.length} possessions. Game and quarter starts: ${ppp(opL)} PPP in ${opL.length}`"),
    ("`Triples abiertos ${mm(op)}, defendidos ${mm(gu)}`", "`Open threes ${mm(op)}, contested ${mm(gu)}`"),
    ("${hb('k','Set')}${hb('n','Jugadas','c-n')}${hb('use','Uso','c-u')}${hb('pts','Puntos','c-p')}${hb('ppp','PPP','c-f')}",
     "${hb('k','Set')}${hb('n','Plays','c-n')}${hb('use','Usage','c-u')}${hb('pts','Points','c-p')}${hb('ppp','PPP','c-f')}"),
    ('<span class="tag sm">muestra pequeña</span>', '<span class="tag sm">small sample</span>'),
    ('<small>Jugadas</small>', '<small>Plays</small>'), ('<small>Uso</small>', '<small>Usage</small>'), ('<small>Puntos</small>', '<small>Points</small>'),
    ('<th>Variante</th><th class="n">Jugadas</th><th class="n">Puntos</th><th class="n">PPP</th><th class="n">Pérdidas</th>',
     '<th>Variant</th><th class="n">Plays</th><th class="n">Points</th><th class="n">PPP</th><th class="n">Turnovers</th>'),
    ('<th>Min. vídeo</th><th>Cuarto</th><th>Nota</th><th>Finaliza</th><th>Resultado</th>', '<th>Video min.</th><th>Quarter</th><th>Note</th><th>Finisher</th><th>Result</th>'),
    ("const DIMS={'Set':'fam','Variante de set':'fv','Tipo de ataque':'cat','Cuarto':'qL','Finaliza':'player'};",
     "const DIMS={'Set':'fam','Set variant':'fv','Type of offense':'cat','Quarter':'qL','Finisher':'player'};"),
    ("selected==null?'Todas las jugadas':selected+' · '+cur.length+' jugadas'", "selected==null?'All plays':selected+' · '+cur.length+' plays'"),
    ("<div class=\"sub\">${pts} puntos en ${list.length} jugadas</div>", "<div class=\"sub\">${pts} points in ${list.length} plays</div>"),
    ('<th>Tipo de saque</th><th class="n">Jug.</th>', '<th>Type of inbound</th><th class="n">Plays</th>'),
    ('<span class="tag">tras tiempo muerto</span>', '<span class="tag">after timeout</span>'),
    ("inbCard('SLOB · saque de banda','SLOB (banda)')+inbCard('BLOB · saque de fondo','BLOB (fondo)')", "inbCard('SLOB · sideline inbounds','SLOB (sideline)')+inbCard('BLOB · baseline inbounds','BLOB (baseline)')"),
    ("<div class=\"sub\">${pts} puntos en ${list.length} posesiones</div>", "<div class=\"sub\">${pts} points in ${list.length} possessions</div>"),
    ("ctxCard('Tras tiempo muerto',PL.filter(p=>p.ato),p=>p.ato)+ctxCard('Inicio de partido y de cuarto',PL.filter(p=>p.qopen),p=>p.qopen==='Q1'?'Inicio de partido':p.qopen+' · inicio')",
     "ctxCard('After timeouts',PL.filter(p=>p.ato),p=>p.ato)+ctxCard('Game and quarter starts',PL.filter(p=>p.qopen),p=>p.qopen==='Q1'?'Game start':p.qopen+' · start')"),
    ("const pct=v=>f1(v,1)+'%';", "const pct=v=>f1(v,1)+'%';"),
    ("['ft','TL']", "['ft','FT']"),
    ("const TT={efg:'Porcentaje efectivo de tiro de campo',pps:'Puntos de campo por tiro',f2:'Tiros de 2: anotados y lanzados',f3:'Tiros de 3: anotados y lanzados',ft:'Tiros libres: anotados y lanzados',sc:'Porcentaje de posesiones con anotación',p1:'Canastas con falta'};",
     "const TT={efg:'Effective field goal percentage',pps:'Field goal points per shot',f2:'2-point shots: made and attempted',f3:'3-point shots: made and attempted',ft:'Free throws: made and attempted',sc:'Share of possessions with a score',p1:'And-ones'};"),
    ("'<th class=\"q\">Quinteto</th>'", "'<th class=\"q\">Lineup</th>'"),
    ("tr(LUO,'tot','Resto de quintetos')+tr(LUT,'tot','Total Fibwi')", "tr(LUO,'tot','Other lineups')+tr(LUT,'tot','Team total')"),
    ("`Mejores: Jackson, More, Matulionis y Lobo con Simeunovic (${f1(LU[0].pps)} PPS) o con Huguet (${f1(LU[1].pps)} PPS)`",
     "`Best: Jackson, More, Matulionis and Lobo with Simeunovic (${f1(LU[0].pps)} PPS) or with Huguet (${f1(LU[1].pps)} PPS)`"),
    ("`Bracey, Kieli y Scariolo con Simeunovic y Huguet: ${f1(LU[2].efg,1)}% EFG, ${f1(LU[2].pps)} PPS`", "`Bracey, Kieli and Scariolo with Simeunovic and Huguet: ${f1(LU[2].efg,1)}% EFG, ${f1(LU[2].pps)} PPS`"),
    ("`Los 4 quintetos con Kieli: ${kieP} puntos de campo en ${kieFGA} tiros (${f1(kieP/kieFGA)} PPS)`", "`The 4 lineups with Kieli: ${kieP} field goal points on ${kieFGA} shots (${f1(kieP/kieFGA)} PPS)`"),
    ("`Entre 1 y 10 tiros por quinteto, leerlo como tendencia`", "`Between 1 and 10 shots per lineup: read it as a trend`"),
    ("a.length?Math.round(100*a.filter(s=>s.made).length/a.length)+'%':'n/d'", "a.length?Math.round(100*a.filter(s=>s.made).length/a.length)+'%':'n/a'"),
    ("[['Triples abiertos',op],['Triples defendidos',gu],['Triples sin etiqueta de defensa',nd],['Tiros de dos',t2]]",
     "[['Open threes',op],['Contested threes',gu],['Threes without a defense tag',nd],['Two-point shots',t2]]"),
    ("[['k','Jugador'],['n','Jugadas'],['pts','Puntos'],['ppp','PPP'],['tovn','Pérdidas']]", "[['k','Player'],['n','Plays'],['pts','Points'],['ppp','PPP'],['tovn','Turnovers']]"),
])
leftover = re.findall(r'(?i)palma|fibwi|estudiantes', re.sub(r'data:[^"\')]+', '', pr.t))
assert not leftover, ('propio: queda Palma', leftover)

# ======================= rival.html =======================
rv = Doc('rival.html')
rv.RS([
    ('<title>Scouting Ourense</title>', '<title>Ourense Scouting</title>'),
    ('<nav aria-label="Secciones">', '<nav aria-label="Sections">'),
    ('<a class="lk" href="#claves">Claves</a>\n    <a class="lk" href="#ataque">Ataque</a>', '<a class="lk" href="#claves">Keys</a>\n    <a class="lk" href="#ataque">Offense</a>'),
    ('<a class="lk" href="#finalizadores">Finalizadores</a>\n    <a class="lk" href="#defensa">Defensa</a>', '<a class="lk" href="#finalizadores">Finishers</a>\n    <a class="lk" href="#defensa">Defense</a>'),
    ('<div class="kick">Informe de scouting · Primera FEB</div>', '<div class="kick">Scouting report · Primera FEB (Spain)</div>'),
    ('aria-label="Partido" id="gsel"><span class="lbl">Partidos</span>', 'aria-label="Game" id="gsel"><span class="lbl">Games</span>'),
    ('<div class="eyebrow">Claves</div>\n    <h2>Lo que <em>apunta</em> el vídeo</h2>', '<div class="eyebrow">Keys</div>\n    <h2>What the <em>video</em> says</h2>'),
    ('<p class="lead">Tres partidos de Ourense (Palencia, Cantabria y Alicante), 524 clips etiquetados. Ataque: 0,89 PPP. Defensa: 0,97 PPP concedido.</p>',
     '<p class="lead">Three Ourense games (Palencia, Cantabria and Alicante), 524 tagged clips. Offense: 0.89 PPP. Defense: 0.97 PPP allowed.</p>'),
])
i = rv.t.index('<div class="three" id="claves-grid">'); j = rv.t.index('</div>\n  </div>\n</section>', i)
rv.t = rv.t[:i] + '''<div class="three" id="claves-grid">
      <div><h4>To attack them</h4><ul><li><b>Shoot off the pass and attack 1-on-1:</b> they allow 1.18 on Spot Up, 1.30 off screens and 1.33 in 1n1.</li><li><b>Crash the offensive glass:</b> 1.44 per possession on their defensive rebound and 1.56 on putbacks.</li><li><b>Run before they get set:</b> 1.37 in transition defense.</li></ul></div>
      <div><h4>To defend them</h4><ul><li><b>Close the offensive glass and the shots off screens:</b> 1.27 and 1.64 PPP.</li><li><b>Stop the early offense:</b> 1n1 EARLY OFFENSE 1.40 and RIM RUNNER 1.50.</li><li><b>Key on #24 Mc Donell, #44 Leimanis and #13 Pinedo:</b> between 1.38 and 1.43 PPP on their actions.</li></ul></div>
    ''' + rv.t[j:]
i = rv.t.index('<div class="three" id="o-read">'); j = rv.t.index('<p class="readnote">', i)
rv.t = rv.t[:i] + '''<div class="three" id="o-read"><div><h4>How they play</h4><ul><li><b>Sets: 34% of their possessions.</b> 90 possessions at 0.80 PPP, below their average (0.89).</li><li><b>Pick and roll outside of sets and transition</b> produce more: 42 possessions at 0.98 without a single turnover, and 41 at 1.02.</li><li><b>Threes:</b> 26 of 76 (34%). On catch-and-shoot (Spot Up), 10 of 39 (26%).</li></ul></div><div><h4>Where they hurt you</h4><ul><li><b>Shots off screens (Off Screen):</b> 22 possessions at 1.64, 7 of 11 from three. Small sample.</li><li><b>Offensive rebounds:</b> 22 possessions at 1.27, 64% with points. Putbacks produce 1.47 in 15.</li><li><b>Finishers:</b> #24 Mc Donell 32 actions at 1.38, #44 Leimanis 21 at 1.38 and #13 Pinedo 14 at 1.43.</li></ul></div><div><h4>Where they get stuck</h4><ul><li><b>Their most used sets produce little:</b> #T6 Side Veer 10 at 0.70, #H1C Iverson Flip Spain 9 at 0.67 and #H2A Horns Roll Smack PnR 8 at 0.75.</li><li><b>FASTBREAK:</b> 16 possessions at 0.56. <b>Sideline inbounds:</b> 21 at 0.67.</li><li><b>Out of sets:</b> 16 possessions at 0.69 and 6 turnovers (38%).</li></ul></div></div>''' + rv.t[j:]
i = rv.t.index('<div class="three" id="d-read">'); j = rv.t.index('<p class="readnote">', i)
rv.t = rv.t[:i] + '''<div class="three" id="d-read"><div><h4>How they defend the pick and roll</h4><ul><li><b>Most tagged coverage: short show</b> (44 actions at 0.91 allowed). Then switch (34 at 0.68), show (14 at 0.79), plug &amp; hedge (10 at 0.50) and under (9 at 1.56).</li><li><b>They contain the PnR ball handler well:</b> 50 actions at 0.76. With switch, 17 at 0.41.</li><li><b>The short show leaves an outlet:</b> against the screener 8 at 1.00 and against the catch-and-shoot 5 at 1.80. Small sample.</li></ul></div><div><h4>Where they struggle</h4><ul><li><b>Transition defense (BALANCE):</b> 27 possessions at 1.37, 63% with points.</li><li><b>Defensive rebounding:</b> 25 actions at 1.44. Putbacks allowed: 16 at 1.56 (81% with points).</li><li><b>Catch-and-shoot:</b> Spot Up 33 at 1.18 (13 of 33 from three). <b>Off screens:</b> 23 at 1.30.</li></ul></div><div><h4>What works for them</h4><ul><li><b>Step Up defense:</b> 43 actions at 0.65 and 8 forced turnovers (19%).</li><li><b>PnR Empty:</b> 10 actions at 0.20. Small sample.</li><li><b>Plug &amp; hedge:</b> 10 at 0.50 with 3 turnovers. <b>Switch:</b> 34 at 0.68.</li></ul></div></div>''' + rv.t[j:]
rv.RS([
    ('<p class="readnote">Lectura de los tres partidos juntos.</p>', '<p class="readnote">Reading of the three games together.</p>', 2),
    ('<div class="eyebrow">Ataque</div><h2>Cómo ataca <em>Ourense</em></h2>', '<div class="eyebrow">Offense</div><h2>How <em>Ourense</em> attacks</h2>'),
    ('<p>#T transición · #H half court · #S sideline · #B baseline</p>', '<p>#T transition · #H half court · #S sideline · #B baseline</p>'),
    ('<h3>Tipo de ataque</h3><p>Barra = posesiones · caja = PPP</p>', '<h3>Type of offense</h3><p>Bar = possessions · box = PPP</p>'),
    ('<h3>Resultado y cuarto</h3><p>Pulsa un tramo o un cuarto para filtrar</p>', '<h3>Result and quarter</h3><p>Click a segment or a quarter to filter</p>'),
    ('aria-label="Ordenar sets" id="s-sort">\n            <span class="lbl">Ordenar</span>\n            <button type="button" data-s="pos" class="on">Frecuencia</button>',
     'aria-label="Sort sets" id="s-sort">\n            <span class="lbl">Sort</span>\n            <button type="button" data-s="pos" class="on">Frequency</button>'),
    ('<button type="button" data-s="ok">% éxito</button>\n            <button type="button" data-s="pts">Puntos</button>', '<button type="button" data-s="ok">% success</button>\n            <button type="button" data-s="pts">Points</button>'),
    ('aria-label="Número de sets" id="s-top">\n            <span class="lbl">Mostrar</span>', 'aria-label="Number of sets" id="s-top">\n            <span class="lbl">Show</span>'),
    ('<button type="button" data-n="0">Todos</button>', '<button type="button" data-n="0">All</button>'),
    ('<span>Set</span><span>Posesiones</span><span>Pos.</span><span>PPP</span><span>Resultado</span>', '<span>Set</span><span>Possessions</span><span>Poss.</span><span>PPP</span><span>Result</span>'),
    ('<h3>Flujo de la jugada</h3><p>Grosor = posesiones · pulsa cualquier bloque para filtrar</p>', '<h3>Play flow</h3><p>Width = possessions · click any block to filter</p>'),
    ('aria-label="Origen" id="k-left"><span class="lbl">Origen</span><button type="button" data-v="set" class="on">Set</button><button type="button" data-v="type">Tipo de ataque</button>',
     'aria-label="Origin" id="k-left"><span class="lbl">Origin</span><button type="button" data-v="set" class="on">Set</button><button type="button" data-v="type">Type of offense</button>'),
    ('aria-label="Destino" id="k-right"><span class="lbl">Destino</span><button type="button" data-v="out" class="on">Resultado</button>',
     'aria-label="Destination" id="k-right"><span class="lbl">Destination</span><button type="button" data-v="out" class="on">Result</button>'),
    ('<h3>Finalizador × playtype</h3><p>Número = posesiones · color = PPP · pulsa celda, jugador o playtype</p>', '<h3>Finisher × playtype</h3><p>Number = possessions · color = PPP · click a cell, player or playtype</p>'),
    ('<i style="background:var(--bad)"></i>PPP bajo</span><span><i style="background:var(--warn)"></i>Medio</span><span><i style="background:var(--good)"></i>Alto</span><span>Intensidad = volumen</span>',
     '<i style="background:var(--bad)"></i>Low PPP</span><span><i style="background:var(--warn)"></i>Medium</span><span><i style="background:var(--good)"></i>High</span><span>Intensity = volume</span>'),
    ('<div class="eyebrow">Defensa</div><h2>Cómo defiende <em>Ourense</em></h2>', '<div class="eyebrow">Defense</div><h2>How <em>Ourense</em> defends</h2>'),
    ('<h3>Cobertura</h3><p>Barra = posesiones · caja = PPP concedido</p>', '<h3>Coverage</h3><p>Bar = possessions · box = PPP allowed</p>'),
    ('<h3>Situación defensiva</h3><p>Barra = posesiones · caja = PPP concedido</p>', '<h3>Defensive situation</h3><p>Bar = possessions · box = PPP allowed</p>'),
    ('<h3>Playtype del rival</h3><p>Acción final contra su defensa</p>', '<h3>Opponent playtype</h3><p>Final action against their defense</p>'),
    ('<h3>Defensor implicado</h3><p>Jugador de Ourense etiquetado en la acción</p>', '<h3>Defender involved</h3><p>Ourense player tagged in the action</p>'),
    ('<h3>Resultado y cuarto</h3><p>Posesiones del rival</p>', '<h3>Result and quarter</h3><p>Opponent possessions</p>'),
    ('<span>Hoop Assistant · Scouting y análisis de vídeo de baloncesto</span>', '<span>Hoop Assistant · Basketball scouting and video analysis</span>'),
    # JS
    ("return 'Saque de fondo'", "return 'Baseline inbounds'"), ("return 'Saque de banda'", "return 'Sideline inbounds'"),
    ("return 'Bloqueo directo'", "return 'Pick and roll'"), ("return 'Transición'", "return 'Transition'"),
    ("return 'Rebote ofensivo'", "return 'Offensive rebound'"), ("return 'Poste'", "return 'Post'"),
    ("return 'Fuera de sistema'", "return 'Out of sets'"), ("return 'Otros'", "return 'Other'"),
    ("const OUT=['Triple anotado','2P anotado','Tiros libres','Triple fallado','2P fallado','Pérdida','Falta recibida','Fuera de banda'];",
     "const OUT=['3PT made','2PT made','Free throws','3PT missed','2PT missed','Turnover','Foul drawn','Out of bounds'];"),
    ("const OSH=['3P ✓','2P ✓','TL','3P ✗','2P ✗','Pérdida','Falta','Fuera'];", "const OSH=['3P ✓','2P ✓','FT','3P ✗','2P ✗','TO','Foul','Out'];"),
    (".toFixed(2).replace('.',',')", ".toFixed(2)"),
    ("O:{type:{l:'Tipo',f:c=>otype(c.cat)},set:{l:'Set',f:c=>/^#|^ATO$/.test(c.cat)?c.cat:null},pl:{l:'Finalizador',f:c=>c.pl},fn:{l:'Playtype',f:c=>c.fn},out:{l:'Resultado',f:c=>OUT[c.o]},q:{l:'Cuarto',f:c=>c.q}}",
     "O:{type:{l:'Type',f:c=>otype(c.cat)},set:{l:'Set',f:c=>/^#|^ATO$/.test(c.cat)?c.cat:null},pl:{l:'Finisher',f:c=>c.pl},fn:{l:'Playtype',f:c=>c.fn},out:{l:'Result',f:c=>OUT[c.o]},q:{l:'Quarter',f:c=>c.q}}"),
    ("D:{cov:{l:'Cobertura',f:c=>c.cov},sit:{l:'Situación',f:c=>c.cat},fn:{l:'Playtype rival',f:c=>c.fn},pl:{l:'Defensor',f:c=>c.pl},out:{l:'Resultado',f:c=>OUT[c.o]},q:{l:'Cuarto',f:c=>c.q}}",
     "D:{cov:{l:'Coverage',f:c=>c.cov},sit:{l:'Situation',f:c=>c.cat},fn:{l:'Opponent playtype',f:c=>c.fn},pl:{l:'Defender',f:c=>c.pl},out:{l:'Result',f:c=>OUT[c.o]},q:{l:'Quarter',f:c=>c.q}}"),
    ("'<p class=\"note\">Sin posesiones con estos filtros.</p>'", "'<p class=\"note\">No possessions with these filters.</p>'", 3),
    ("${g.pos} posesiones · ${g.pts} pts<br>${f2(g.ppp)} PPP · ${pc(g.ok*g.pos,g.pos)} éxito", "${g.pos} possessions · ${g.pts} pts<br>${f2(g.ppp)} PPP · ${pc(g.ok*g.pos,g.pos)} success"),
    ("<small>Resultado</small><b>${OUT[i]}</b>${cnt[i]} posesiones · ${pc(cnt[i],tot)}", "<small>Result</small><b>${OUT[i]}</b>${cnt[i]} possessions · ${pc(cnt[i],tot)}"),
    ("<span>${q.replace('Q','º cuarto')}</span>", "<span>Q${q.replace('Q','')}</span>"),
    ("[[a.pos,'Posesiones'],[f2(a.ppp),D?'PPP concedido':'PPP'],[a.pts,D?'Puntos concedidos':'Puntos'],[pc(a.ok*a.pos,a.pos),D?'% éxito rival':'% éxito'],[pc(a.to,a.pos),D?'% pérdidas forzadas':'% pérdidas']]",
     "[[a.pos,'Possessions'],[f2(a.ppp),D?'PPP allowed':'PPP'],[a.pts,D?'Points allowed':'Points'],[pc(a.ok*a.pos,a.pos),D?'% opponent success':'% success'],[pc(a.to,a.pos),D?'% forced turnovers':'% turnovers']]"),
    ("b('Más usado · '+label,most.k,pc(most.pos,a.pos))+b(D?'Más concede':'Mejor PPP',hi.k,f2(hi.ppp),D?'var(--bad)':'var(--good)')+(lo!==hi?b(D?'Menos concede':'Peor PPP',lo.k,f2(lo.ppp),D?'var(--good)':'var(--bad)'):'')",
     "b('Most used · '+label,most.k,pc(most.pos,a.pos))+b(D?'Allows most':'Best PPP',hi.k,f2(hi.ppp),D?'var(--bad)':'var(--good)')+(lo!==hi?b(D?'Allows least':'Worst PPP',lo.k,f2(lo.ppp),D?'var(--good)':'var(--bad)'):'')"),
    ("`<p class=\"note\">${total-sN} sets más ocultos.</p>`", "`<p class=\"note\">${total-sN} more sets hidden.</p>`"),
    ("${g.pos} pos · ${g.pts} pts · ${f2(g.ppp)} PPP · ${pc(g.ok*g.pos,g.pos)} éxito<br>", "${g.pos} poss · ${g.pts} pts · ${f2(g.ppp)} PPP · ${pc(g.ok*g.pos,g.pos)} success<br>"),
    ("mv=c=>c.pl[0]||'Sin jugador', rv=c=>kR==='out'?OUT[c.o]:(c.fn[0]||'Sin playtype');", "mv=c=>c.pl[0]||'No player', rv=c=>kR==='out'?OUT[c.o]:(c.fn[0]||'No playtype');"),
    ("const L=c=>keep.has(lv(c))?lv(c):'Otros';", "const L=c=>keep.has(lv(c))?lv(c):'Others';"),
    ("(a[0]==='Otros'||a[0].startsWith('Sin '))-(b[0]==='Otros'||b[0].startsWith('Sin '))", "(a[0]==='Others'||a[0].startsWith('No '))-(b[0]==='Others'||b[0].startsWith('No '))"),
    ("aria-label=\"Flujo de posesiones\"", "aria-label=\"Possession flow\""),
    ("[['Origen',X[0]],['Finalizador',X[1]],[kR==='out'?'Resultado':'Playtype',X[2]]]", "[['Origin',X[0]],['Finisher',X[1]],[kR==='out'?'Result':'Playtype',X[2]]]"),
    ("click=!(n.k==='Otros'||n.k.startsWith('Sin '))", "click=!(n.k==='Others'||n.k.startsWith('No '))"),
    ("if(!(k==='Otros'||k.startsWith('Sin ')))", "if(!(k==='Others'||k.startsWith('No ')))"),
    ("${n.v} posesiones · ${pc(n.v,rs.length)}", "${n.v} possessions · ${pc(n.v,rs.length)}"),
    ("<small>${x.s==='O'?'Ataque':'Defensa'} · ${DIMS[x.s][x.d].l}</small>", "<small>${x.s==='O'?'Offense':'Defense'} · ${DIMS[x.s][x.d].l}</small>"),
    ("'<button type=\"button\" class=\"chip clear\" id=\"clr\">Limpiar todo</button>':'<span class=\"hint\">Pulsa cualquier barra, bloque o celda para filtrar</span>'",
     "'<button type=\"button\" class=\"chip clear\" id=\"clr\">Clear all</button>':'<span class=\"hint\">Click any bar, block or cell to filter</span>'"),
    ("<span>PPP ataque</span></div><div><b class=\"num\">${f2(ad.ppp)}</b><span>PPP concedido</span></div><div><b class=\"num\">${ao.pts} / ${ad.pts}</b><span>Puntos</span></div><div><b class=\"num\">${ao.pos}</b><span>Posesiones ataque</span>",
     "<span>Offense PPP</span></div><div><b class=\"num\">${f2(ad.ppp)}</b><span>PPP allowed</span></div><div><b class=\"num\">${ao.pts} / ${ad.pts}</b><span>Points</span></div><div><b class=\"num\">${ao.pos}</b><span>Offensive possessions</span>"),
    ("badges('#o-badges','O','type','tipo')", "badges('#o-badges','O','type','type')"),
    ("badges('#d-badges','D','cov','cobertura')", "badges('#d-badges','D','cov','coverage')"),
    ("`<span class=\"pend\">Partido ${done+i+1} · pendiente</span>`", "`<span class=\"pend\">Game ${done+i+1} · pending</span>`"),
    ("`<button type=\"button\" data-g=\"all\" class=\"on\">Todos (${done})</button>`", "`<button type=\"button\" data-g=\"all\" class=\"on\">All (${done})</button>`"),
    ("`${C.length} clips etiquetados · ${done} de ${EXPECTED} partidos`", "`${C.length} tagged clips · ${done} of ${EXPECTED} games`"),
])

# ======================= salida =======================
if os.path.exists(OUT):
    shutil.rmtree(OUT)
shutil.copytree(os.path.join(SRC, 'assets'), os.path.join(OUT, 'assets'))
shutil.copytree(os.path.join(SRC, 'jugadores'), os.path.join(OUT, 'jugadores'))
ix.save(); pr.save(); rv.save()
print('ok')
