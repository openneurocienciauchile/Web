# Informe de busqueda de ORCID iD -- academicos del Departamento

Generado por `scripts/buscar_orcid_academicos.py` el 25 de agosto de 2026 y **revisado
a mano** despues (ver "Correcciones tras la revision").

## Estado actual

**32 de 34** academicos ya tienen su ORCID iD en su ficha.
Quedan 2 sin iD: Marco Elvis Contreras Abarca y Nicole Andrea Rogers Castillo.

## Rellenados cruzando con Neurosistemas

Misma persona en ambos sitios; el iD ya estaba confirmado alla.

| Persona | ORCID iD |
|---|---|
| Christ Alejandra Devia Manriquez | [0000-0002-2416-0864](https://orcid.org/0000-0002-2416-0864) |

## Rellenados desde la API de ORCID (unico candidato con afiliacion U. de Chile)

Se verificaron uno por uno contra `/person`, `/employments` y `/works` de la API publica.

| Persona | ORCID iD | Verificacion | Obras publicas |
|---|---|---|---|
| Andres Oscar Couve Correa | [0009-0009-2520-3895](https://orcid.org/0009-0009-2520-3895) | ORCID dice "Andres Couve"; declara Mount Sinai, PUC, U. de Chile, UCL | **0** (perfil vacio) |
| Catherine Maria Perez Valenzuela | [0009-0007-1960-3089](https://orcid.org/0009-0007-1960-3089) | ORCID dice "Catherine Perez-Valenzuela"; U. de Chile | **0** (perfil vacio) |
| Gonzalo Andres Farias Gontupil | [0000-0002-7979-8398](https://orcid.org/0000-0002-7979-8398) | Alzheimer, Parkinson, locus coeruleus, biomarcadores -- calza con su ficha | 52 |
| Pablo Felipe Henny Vargas | [0000-0001-8470-8222](https://orcid.org/0000-0001-8470-8222) | ORCID dice "Pablo Henny"; declara Oxford, McGill, PUC, U. de Chile | **0** (perfil vacio) |
| Rodrigo Antonio Nieto Rojas | [0000-0002-4598-8951](https://orcid.org/0000-0002-4598-8951) | BDNF, esquizofrenia, bipolaridad, realidad virtual -- calza con su ficha | 7 |

Los tres perfiles con **0 obras publicas** tienen el iD correcto, pero no aportaran nada al
listado de `/publicaciones/` ni al bloque "Desde ORCID" de su ficha hasta que esas personas
suban sus trabajos a ORCID. No es un error del sincronizador.

## Correcciones tras la revision

### Cecilia Hidalgo -- falso positivo corregido

El script autocompleto `0000-0002-6497-9014`, que **NO es ella**: ese perfil pertenece a
*Maria Gabriela Hidalgo Gorostegui* (0 obras, afiliacion COANIQUEM). Paso porque la
busqueda acotada a "Universidad de Chile" devolvio un unico resultado y el apellido
principal calzaba, mientras que el perfil real no aparecia en esa consulta (la ficha dice
"Maria Cecilia Margarita", y su perfil ORCID esta a nombre de "Cecilia" a secas).

Se revirtio y se aplico el correcto, confirmado a mano:

| Persona | ORCID iD | Verificacion | Obras publicas |
|---|---|---|---|
| Maria Cecilia Margarita Hidalgo Tapia | [0000-0003-1256-9651](https://orcid.org/0000-0003-1256-9651) | Empleo declarado "Universidad de Chile, profesor/a"; obras sobre receptores de rianodina, senalizacion de calcio, hipocampo, ferroptosis -- calza exacto con su ficha | 19 |

### Tres pendientes aplicados tras confirmacion de Hayo

Eran candidato unico pero el script no los autocompleto porque no declaran afiliacion
"Universidad de Chile" en ORCID. Revisados y aprobados el 25 de agosto de 2026:

| Persona | ORCID iD | Verificacion | Obras publicas |
|---|---|---|---|
| Gonzalo Alberto Olivares Herane | [0000-0002-2784-0160](https://orcid.org/0000-0002-2784-0160) | Declara "Univerdidad de Chile" (con typo, por eso no lo pillo la busqueda) y Universidad Mayor; obras sobre poliadenilacion alternativa, Drosophila y nutricion temprana -- calce exacto con su ficha, que menciona "procesamiento alternativo de mRNAs", "Drosophila" y el "Fly Research Hub" de la U. Mayor | 24 |
| Hachi Eben ElHaggch Manzur Valdivia | [0000-0001-6287-4326](https://orcid.org/0000-0001-6287-4326) | Nombre practicamente unico y candidato unico; obras sobre estrategias de aprendizaje en ratas, microestimulacion de corteza sensorial y kinesiologia. Su ficha esta "en preparacion", asi que no se pudo contrastar por temas | 5 |
| Manuel Arturo Kukuljan Padilla | [0000-0001-9927-6696](https://orcid.org/0000-0001-9927-6696) | Apellido unico, nombre exacto, candidato unico. Perfil vacio: sin afiliacion declarada y **0 obras** | **0** (perfil vacio) |

## Pendientes: sin candidato defendible

Los candidatos que devolvio la API son homonimos de otras areas. Se dejan **sin** el campo
`orcid` a proposito; lo mas simple es pedirle su iD a cada persona y cargarlo por Pages CMS
(campo ORCID de la ficha).

### Marco Elvis Contreras Abarca

Ninguno de los dos candidatos es el academico del Departamento (su ficha es neurociencia
cognitiva):

| ORCID iD | Nombre en ORCID | Por que se descarto |
|---|---|---|
| [0000-0002-0518-1037](https://orcid.org/0000-0002-0518-1037) | Marco Contreras | Ingenieria forestal (cosecha mecanizada, plantaciones de pino, LiDAR); U. Austral y U. de Kentucky |
| [0000-0002-9508-546X](https://orcid.org/0000-0002-9508-546X) | Marco Contreras-Castro | Linguistica y educacion en ingenieria (marcadores conversacionales, analisis del discurso); PUC y U. de Las Americas |

### Nicole Andrea Rogers Castillo

Ningun perfil corresponde. Su ficha es navegacion espacial y deterioro cognitivo temprano:

| ORCID iD | Nombre en ORCID | Por que se descarto |
|---|---|---|
| [0009-0004-3391-8720](https://orcid.org/0009-0004-3391-8720) | "Nicole Andrea" | Perfil vacio, sin apellido Rogers, 0 obras |
| [0009-0008-2675-4173](https://orcid.org/0009-0008-2675-4173) | "Andrea Nicole Andrea" | Universidad Nacional Federico Villarreal (Peru), 0 obras |

## Nota sobre volver a correr el script

`buscar_orcid_academicos.py` solo toca fichas que **no** tienen `orcid`, asi que volver a
correrlo no reintroduce el falso positivo de Cecilia Hidalgo ni pisa nada de lo corregido
aqui. Solo reintentaria a Marco Contreras y Nicole Rogers.
