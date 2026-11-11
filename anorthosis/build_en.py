"""Genera index.html (inglés, Anorthosis) a partir de la propuesta en español."""
import json, re, os
H = os.path.dirname(os.path.abspath(__file__))
es = open(os.path.join(H, '_es.html'), encoding='utf-8').read()
body = open(os.path.join(H, '_body_en.html'), encoding='utf-8').read()
A = json.load(open(os.path.join(H, '_assets.json')))
i, j = es.index('<nav aria-label="Secciones">'), es.index('<script>')
t = es[:i] + body + es[j:]

def R(a, b, n=1):
    global t
    c = t.count(a)
    assert c == n, (a[:70], c)
    t = t.replace(a, b)

# ---- head ----
R('<html lang="es">', '<html lang="en">')
R('<title>Hoop Assistant × Fibwi Palma</title>', '<title>Hoop Assistant × Anorthosis</title>')
R('content="Propuesta de Hoop Assistant para Fibwi Palma: scouting propio, rival en ataque, rival en defensa y jugadores, con datos."',
  'content="Hoop Assistant proposal for Anorthosis Famagusta BC: self-scouting, opponent offense, opponent defense and players, with data."')

# ---- botón 'Clear selection' visible sin selección ----
t = t.replace('</style>', '.selname button[hidden]{display:none}\n</style>', 1)

# ---- formato de números ----
R(".toFixed(2).replace('.',',')", ".toFixed(2)")
R("toLocaleString('es-ES')", "toLocaleString('en-GB')", 2)
R("<b class=\"num ${s[3]||''}\">${String(s[1]).replace('.',',')}</b>${s[2]?`<small class=\"num\">${String(s[2]).replace(/\\./g,',')}</small>`:''}",
  "<b class=\"num ${s[3]||''}\">${s[1]}</b>${s[2]?`<small class=\"num\">${s[2]}</small>`:''}")
R("${String(p[6]).replace('.',',')} pts", "${p[6]} pts")

# ---- OER y escalera ----
for a, b in [("['Contraataque',11,", "['Fast break',11,"), ("['Llegada',3,", "['Early offense',3,"), ("['Otras de llegada',2,", "['Other early offense',2,"),
             ("['Rebote ofensivo',11,", "['Offensive rebound',11,"), ("['Opción rápida',7,", "['Quick option',7,"), ("['Opción organizada',4,", "['Organized option',4,"),
             ("['Transición',1,", "['Transition',1,"), ("['Drag PnP con 4',1,", "['Drag PnP with 4',1,"), ("['Bloqueo directo',14,", "['Pick and roll',14,"),
             ("['PnR con 4',1,", "['PnR with 4',1,"), ("['Saque de fondo (BLOB)',6,", "['Baseline inbounds (BLOB)',6,"),
             ("['Saque de banda (SLOB)',12,", "['Sideline inbounds (SLOB)',12,"), ("['Otras',11,", "['Other',11,")]:
    R(a, b)
R("const rows=[['Contraataque',1.30],['Bloqueo directo',1.15],['Rebote ofens.',.91],['Sets',.76],['Otras',.27]];",
  "const rows=[['Fast break',1.30],['Pick and roll',1.15],['Off. rebound',.91],['Sets',.76],['Other',.27]];")
R("'Contraataque':[14,4],'Otras':[14,4]", "'Fast break':[14,4],'Other':[14,4]")
R("${s[1]} posesiones · ${f2(ppp)} PPP<br>${s[3]} puntos", "${s[1]} possessions · ${f2(ppp)} PPP<br>${s[3]} points")
R("xl:'Posesiones (frecuencia)',yl:'Puntos por posesión',aria:'Dispersión de acciones del rival por frecuencia y eficiencia'",
  "xl:'Possessions (frequency)',yl:'Points per possession',aria:'Opponent actions by frequency and efficiency'")
R("quads:[['r','t','Mucho uso · PPP alto'],['l','t','Poco uso · PPP alto'],['r','b','Mucho uso · PPP bajo'],['l','b','Poco uso · PPP bajo']]",
  "quads:[['r','t','High use · high PPP'],['l','t','Low use · high PPP'],['r','b','High use · low PPP'],['l','b','Low use · low PPP']]")

# ---- panel propio ----
R("const gname=g=>'J'+(g+1)+' '+P.games[g][0];", "const gname=g=>'R'+(g+1)+' '+P.games[g][0];")
R("q:r=>r[2]?r[2]+'º cuarto':'Sin cuarto'", "q:r=>r[2]?'Q'+r[2]:'No quarter'")
R("if(ev==='BIEN')b++;else if(ev==='MAL')m++", "if(ev==='GOOD')b++;else if(ev==='BAD')m++")
R("'Barra = PPP · número pequeño = posesiones':lm==='pos'?'Barra = posesiones etiquetadas':'Barra = % de clips valorados bien por el staff'",
  "'Bar = PPP · small number = possessions':lm==='pos'?'Bar = tagged possessions':'Bar = % of clips rated good by the staff'")
R("'<p class=\"note\">Ningún grupo llega al mínimo de posesiones. Bajad el mínimo.</p>'", "'<p class=\"note\">No group reaches the minimum possessions. Lower the minimum.</p>'")
R("g.val+' val'", "g.val+' rated'")
R("$('#lab-sel').textContent=g?g.k:'Toda la temporada';", "$('#lab-sel').textContent=g?g.k:'Whole season';")
R("class=\"${ev==='BIEN'?'ok':ev==='MAL'?'ko':''}\">${ev==='Sin valorar'?'–':ev}</td>", "class=\"${ev==='GOOD'?'ok':ev==='BAD'?'ko':''}\">${ev==='Not rated'?'–':ev}</td>")
R("`Ver más clips (${(list.length-lshow).toLocaleString('en-GB')} restantes)`", "`Show more clips (${(list.length-lshow).toLocaleString('en-GB')} left)`")
R("${g[1]?'Local':'Visitante'}", "${g[1]?'Home':'Away'}")
R("<span>Posesiones</span></div><div><b class=\"num\">${f2(a.ppp)}${d(a.ppp,b.ppp,f2)}</b><span>PPP · temporada ${f2(b.ppp)}</span></div><div><b class=\"num\">${pc(a.ok)}</b><span>% bien · temporada ${pc(b.ok)}</span>",
  "<span>Possessions</span></div><div><b class=\"num\">${f2(a.ppp)}${d(a.ppp,b.ppp,f2)}</b><span>PPP · season ${f2(b.ppp)}</span></div><div><b class=\"num\">${pc(a.ok)}</b><span>% good · season ${pc(b.ok)}</span>")
R("title=\"Temporada ${f2(x.s.ppp)}\"", "title=\"Season ${f2(x.s.ppp)}\"")
R("title=\"Partido ${f2(x.a.ppp)}\"", "title=\"Game ${f2(x.a.ppp)}\"")
R("<span>0 PPP</span><span>1,5</span><span>3 PPP</span>", "<span>0 PPP</span><span>1.5</span><span>3 PPP</span>")
R("const mal=gm.filter(r=>D.ev[r[7]]==='MAL');", "const mal=gm.filter(r=>D.ev[r[7]]==='BAD');")
R("<td>${r[2]?r[2]+'º':'–'}</td>", "<td>${r[2]?'Q'+r[2]:'–'}</td>")
R("`<tr><td colspan=\"5\" style=\"color:var(--muted)\">y ${mal.length-12} clips más</td></tr>`", "`<tr><td colspan=\"5\" style=\"color:var(--muted)\">and ${mal.length-12} more clips</td></tr>`")
R("'<tr><td colspan=\"5\" style=\"color:var(--muted)\">Ningún clip valorado mal en este partido.</td></tr>'", "'<tr><td colspan=\"5\" style=\"color:var(--muted)\">No clips rated bad in this game.</td></tr>'")

# ---- materiales ----
R("off:['v','Offensive Scouting','Vídeo ofensivo']", "off:['v','Offensive Scouting','Offensive video']")
R("scout:['v','Video Scout','Vídeo de scouting de equipo']", "scout:['v','Video Scout','Team scouting video']")
R("oer:['p','OER Report','Informe de eficiencia ofensiva']", "oer:['p','OER Report','Offensive efficiency report']")
R("def:['v','Defensive Scouting','Vídeo defensivo']", "def:['v','Defensive Scouting','Defensive video']")
R("defr:['p','Defensive Scouting Report','Informe defensivo']", "defr:['p','Defensive Scouting Report','Defensive report']")
R("ply:['v','Player Scouting','Vídeo de jugadores']", "ply:['v','Player Scouting','Player video']")
R("plr:['p','Player Report','Informe de jugadores']", "plr:['p','Player Report','Player report']")
R("</svg>Vídeo':'PDF'}", "</svg>Video':'PDF'}")
R("Abrir en Drive ↗", "Open in Drive ↗")

# ---- coberturas ----
i = t.index('const COV=['); j = t.index('];', i) + 2
t = t[:i] + """const COV=[
  ['flat','High Flat','They struggle, especially with #20 Fiorentino defending the screener: lateral problems, he goes too high and too far in front of the ball. They want to avoid the screen and chase the ball handler. The last defender is usually ready for the roll, but the X-man is late rotating to the corner.','Pass to the short roll and the rotation to the corner.'],
  ['show','Show','On Side PnR they collapse heavily with the weak-side defender. Little ball pressure and a lot of space between the screen and the ball handler. #20 Fiorentino is late on the show. Same rotation problems as in High Flat.','Pass to the short roll, and the weak-side shot if that defender collapses.'],
  ['drop','Drop (Over)','The screener\\'s defender clearly prioritizes the ball. Opponents have struggled against it because they did not screen effectively.','Good spacing and an effective screen.'],
  ['under','Under','Only against specific players: they used it against Marius Stoll (#9, Schwelm). On the re-screen, Under or Show.',''],
  ['four','PnR with the 4','Flat (lower than with the centers) or switch. In Flat they can struggle on closeouts after the pop. When they switch, they defend the mismatches well.','Pop and closeout when they play Flat.']
];""" + t[j:]
R("<span class=\"lab\">Lo que vimos</span>", "<span class=\"lab\">What we saw</span>")
R("<span class=\"lab\">Dónde sufren</span>", "<span class=\"lab\">Where they struggle</span>")

# ---- jugadores (texto original del informe, en inglés) ----
i = t.index('const PL=['); j = t.index('];\n', i) + 3
t = t[:i] + """const PL=[
 [9,'PG','David Ewald',26,'1.85',29,6.8,2.1,3.3,63.9,.5,2.2,23.6,1,1.5,63.2,3.8,3.3,.5,4.8,1.8,1.6,12.4,['His main action is PnR ball handler. Attacks with speed and can use both hands.','Watch out for the <mark>REJECT</mark>, especially to his right.','On closeouts and in the open court he attacks aggressively, looking to <mark>finish at the rim</mark>.','His go-to move is the slow step, especially when attacking closeouts.']],
 [8,'SG','Bryant Allen',36,'1.80',34,15.3,3.4,7.1,47.2,2.2,5.7,38.6,2,2.4,83.3,3.1,2.5,.6,3,1.8,1.9,13.7,['<mark>Left-handed driver</mark>: attacks left with speed. If he goes right, he usually takes a pull-up.','PnR ball handler: mainly looks to score left-handed or pass to the roll. Not a playmaker.','<mark>Catch &amp; shoot threat</mark>: do not let him shoot comfortably.','Weak off-ball defense: vulnerable to cuts and backdoors.']],
 [22,'SF','Faton Jetullahi',32,'1.89',31,11,1.6,3.4,45.6,2,6.2,33.1,1.7,2.4,70.9,4.3,4,.3,3,1.4,1.9,11,['Comfortable <mark>shooting off the dribble</mark>: do not play UNDER.','Creative PnR passer, especially finding the big on the roll.','Great <mark>catch and shoot player</mark>, particularly when left open.','Looks for contact when he attacks the rim.']],
 [11,'PF','Christian Hinckson',26,'2.01',24,13.8,2.9,5.2,56,1.5,3.7,41.6,3.3,4.1,81.6,4.9,3.7,1.3,1.5,1,1.6,14.9,['His biggest threat is as a PnR roller: he can <mark>pop</mark> for catch and shoot or punish switches by rolling.','Finishes with both hands, <mark>shoots spot-ups and attacks closeouts after popping</mark>.','Defensively: great lateral mobility and strength. Pump fakes are the best way to beat him.']],
 [20,'C','Dario Fiorentino',39,'2.06',30,11.1,2.1,4.9,43.4,1.4,4.2,34.6,2.5,3.4,73.3,5.3,4.3,1,1,.6,1.4,10.6,['<mark>Slips</mark> the PnR to roll straight to the rim, prefers right-hand finishes.','On contact screens or late in the possession he <mark>pops</mark>: deep three-point range.','Defensively he has <mark>lateral issues</mark> and gives up space for the short roll pass.']],
 [44,'PG','Müslim Özmeral',25,'1.85',22,4.5,1.4,2.3,58.8,.4,1.8,20.5,.7,.8,88.9,2.5,1.9,.5,1.4,.6,1.4,5.2,['Great first step and speed: beats defenders immediately.','In the PnR he often looks to <mark>REJECT</mark> and use his speed.','<mark>Aggressive on-ball defender</mark>: high motor, but not always reliable 1-on-1.']],
 [10,'PF','Gilbert Gyamfi',34,'1.93',20,7.8,1.7,3.5,48.9,1,3.4,28.4,1.5,2,74.5,3.9,2.6,1.3,.9,.7,1.6,7.5,['Left-handed, <mark>very quick and agile</mark>: prefers going left and finishing with a Eurostep.','Likes contact finishes, especially in <mark>open-court actions</mark>.','Can shoot off spot-ups or flare actions after horns. Capable of taking tough shots.']],
 [0,'SG','Esosa Okundaye',33,'1.87',15,5.8,1,2.3,44.4,.8,2.4,31.6,1.5,1.6,92.3,1.6,1.3,.4,.5,.1,1.1,4,['Great first step: attacks right-handed and looks to <mark>finish through contact</mark>.','Uses physicality to create an advantage before attacking.','His best catch and shoot spot is the right wing.']],
 [14,'C','Tarik Jakupovic',25,'2.03',13,4.9,1.8,3.5,52.4,0,.3,0,1.3,1.8,69.7,2.7,1.6,1.1,.2,.2,.7,5,['Always rolls and looks to finish without dribbling. No shooting range.','Great <mark>offensive rebounder</mark> and strong cutter near the rim.','Prefers playing without the dribble, especially around the basket.']],
 [21,'PG','Tim Elkehans',26,'1.80',12,2.1,.4,1,36,.3,.8,38.9,.5,.7,70.6,.5,.2,.3,.7,.5,.8,1.5,['<mark>Pass-first PnR handler</mark>: looks for the roll first, and the mid-range when finishing.','Catch and shoot threat from the corners, with a quick release.','Does not look to take many shots.']],
 [35,'PG','Manuel Bojang',25,'1.85',8,.7,0,.7,0,0,.7,0,.7,.7,100,.7,.7,0,.3,0,1.3,-1,['Rotation point guard.']],
 [24,'SG','Stefan Bogdan',20,'1.96',6,.4,.2,.6,28.6,0,.1,0,.1,.1,100,.8,.5,.3,.4,.2,.2,1.2,['Rotation shooting guard.']]
];
""" + t[j:]
R("['TL%',p[15],", "['FT%',p[15],")
R("`${p[17]} def · ${p[18]} of`", "`${p[17]} def · ${p[18]} off`")
R("['Ast',p[19],`${p[20]} rob · ${p[21]} pér`],['Val',p[22],'']", "['Ast',p[19],`${p[20]} stl · ${p[21]} TO`],['Eff',p[22],'']")
R("${p[3]} años · ${p[4]} m", "${p[3]} y/o · ${p[4]} m")
R("xl:'Puntos por partido',yl:'TS%',aria:'Puntos por partido frente a TS% de cada jugador'", "xl:'Points per game',yl:'TS%',aria:'Points per game vs TS% for each player'")
R("quads:[['r','t','Más puntos · más TS%'],['l','b','Menos puntos · menos TS%']]", "quads:[['r','t','More points · higher TS%'],['l','b','Fewer points · lower TS%']]")

# ---- copiar correo ----
R("$('#copy').textContent='Copiado'", "$('#copy').textContent='Copied'")
R("$('#copy').textContent='Seleccionado: pulsad copiar'", "$('#copy').textContent='Selected: press copy'")
R("$('#copy').textContent='Copiar correo'", "$('#copy').textContent='Copy email'")

# ---- datos del panel propio ----
P = json.loads(A['P'])
tr = {'ty': {'Transición': 'Transition'}, 'pg': {'Sin base': 'No PG'}, 'ev': {'Sin valorar': 'Not rated', 'BIEN': 'GOOD', 'MAL': 'BAD'},
      'pl': {'Sin jugador': 'No player'}, 'st': {'TRANSICIÓN': 'TRANSITION'}}
for k, m in tr.items():
    P['dic'][k] = [m.get(x, x) for x in P['dic'][k]]
P['out'] = ['3PT made', '2PT made', 'Free throws', '3PT missed', '2PT missed', 'Turnover', 'Foul drawn', 'No result']
t = t.replace('__PROPIO__', json.dumps(P, ensure_ascii=False, separators=(',', ':')))

# ---- imágenes ----
it = iter(A['uris'])
t = re.sub('DATAURI', lambda m: next(it), t)
open(os.path.join(H, 'index.html'), 'w', encoding='utf-8').write(t)
i = t.index('<nav ')
j = t.index('</body>')
art = t[t.index('<title>'):t.index('</head>')] + t[t.index('<body>') + 6:j]
open(os.path.join(H, 'index.artifact.html'), 'w', encoding='utf-8').write(art)
print('ok', len(t))
