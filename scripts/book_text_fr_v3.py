"""
Stella & Yakob — Version 3 (45 pages)
French text — pages 1-30 preserved, pages 31-45 new
"""

PAGES = [
    # ── ACT 1: The Fear (pages 1–3) ───────────────────────────────────────
    (1, [
        "Le jardin de Stella était gris ce soir-là.",
        "Les fleurs penchaient la tête.",
        "Quelque chose dans l'air sentait l'inquiétude.",
    ]),
    (2, [
        "Par la fenêtre embuée,",
        "Stella entendait ses parents parler.",
        "« Intelligence artificielle. » « Emplois. » « Peur. »",
        "Des mots qu'elle ne comprenait pas.",
    ]),
    (3, [
        "Stella s'assit dans l'herbe, les genoux serrés.",
        "Une larme roula sur sa joue.",
        "« Si les machines savent tout faire…",
        "à quoi je sers, moi ? »",
    ]),

    # ── ACT 1: Yakob arrives (pages 4–7) ──────────────────────────────────
    (4, [
        "Alors le grand chêne brilla doucement.",
        "Et sur la branche la plus haute,",
        "deux yeux ambrés s'ouvrirent dans la nuit.",
    ]),
    (5, [
        "L'hibou pencha la tête.",
        "Des étincelles dorées dansèrent dans l'air.",
        "« Je m'appelle Yakob », dit-il.",
        "« Et ta question mérite un long voyage. »",
    ]),
    (6, [
        "Stella leva les yeux vers lui.",
        "« Papa risque de perdre son travail »,",
        "dit-elle tout bas.",
        "Yakob hocha la tête avec douceur.",
        "« Viens. Il y a des choses à voir. »",
    ]),
    (7, [
        "Yakob déploya ses grandes ailes.",
        "Une poussière dorée tourbillonna autour d'eux.",
        "Le jardin gris disparut.",
        "L'aventure commença.",
    ]),

    # ── ACT 1: Journey through time (pages 8–10) ──────────────────────────
    (8, [
        "Ils se retrouvèrent dans une grotte ancienne.",
        "Des mains humaines étaient dessinées sur les parois,",
        "rouges et ocres, depuis des milliers d'années.",
        "« Voilà le premier outil », dit Yakob.",
        "« Une image. Une idée partagée. »",
    ]),
    (9, [
        "Des lettres s'envolèrent comme des papillons.",
        "Elles montèrent très haut dans le ciel blanc.",
        "« L'alphabet. L'imprimerie. Le téléphone. »",
        "« Chaque invention a changé le monde. »",
        "« Et pourtant — les humains sont restés. »",
    ]),
    (10, [
        "Une ampoule dorée brilla au centre.",
        "Stella et un autre enfant tenaient",
        "des fils de lumière dans leurs mains.",
        "« L'électricité n'a pas volé la flamme. »",
        "« Elle l'a rendue plus lumineuse. »",
    ]),

    # ── ACT 1: What is AI? (pages 11–13) ──────────────────────────────────
    (11, [
        "Un petit robot rond et doux apparut.",
        "À ses pieds, des piles de dessins :",
        "chiens, chats, lapins, oiseaux.",
        "« Il apprend », dit Yakob.",
        "« Comme toi — mais différemment. »",
    ]),
    (12, [
        "Le robot attrapa le dessin d'un chien…",
        "et le posa dans la pile des chats !",
        "Stella éclata de rire, la main sur la bouche.",
        "Yakob inclina la tête, amusé.",
        "« Elle se trompe aussi, tu vois. »",
    ]),
    (13, [
        "Un médecin souriait à un petit enfant.",
        "Un drone déposait une graine dans la terre.",
        "Un musicien jouait avec un logiciel lumineux.",
        "« L'IA peut aider à soigner, planter, créer. »",
        "« Mais elle a besoin de toi pour choisir. »",
    ]),

    # ── ACT 1: The hard question (pages 14–16) ────────────────────────────
    (14, [
        "Stella posa la main sur sa poitrine.",
        "« Mais… si les machines font tout, »",
        "dit-elle tout bas,",
        "« à quoi servent les gens ? »",
        "Les lumières autour d'elles s'assombrirent un peu.",
    ]),
    (15, [
        "Yakob baissa sa grande tête vers Stella.",
        "Ses yeux ambrés étaient doux et graves.",
        "« Une machine peut dessiner un visage. »",
        "« Mais peut-elle aimer ce visage ? »",
        "Stella ne répondit pas. Elle réfléchissait.",
    ]),
    (16, [
        "Un homme en chapeau haut-de-forme",
        "allumait un réverbère à gaz.",
        "À côté, une lampe électrique s'allumait seule.",
        "« Les allumeurs de réverbères ont disparu, »",
        "dit Yakob. « Mais la lumière est restée. »",
    ]),

    # ── ACT 1: Silver Fox twist (pages 17–22) ─────────────────────────────
    (17, [
        "Soudain, des buissons surgit une silhouette.",
        "Un renard élégant, à la fourrure argentée.",
        "Il avait un sourire un peu trop large.",
        "« Bonjour, Stella. Je connais tes peurs. »",
        "« Et j'ai quelque chose pour toi. »",
    ]),
    (18, [
        "Le renard tournait autour de Stella,",
        "sa voix douce comme de la soie.",
        "« Pourquoi apprendre, si je peux tout savoir ? »",
        "« Pourquoi chercher, si j'ai déjà les réponses ? »",
        "Yakob resta silencieux, les yeux mi-clos.",
    ]),
    (19, [
        "Un chemin argenté s'étendait devant elles.",
        "Des fleurs de verre scintillaient sur les bords.",
        "Tout était parfait. Tout était froid.",
        "« Viens, dit le renard. Tu n'auras plus jamais peur. »",
    ]),
    (20, [
        "Stella s'arrêta.",
        "Elle baissa les yeux.",
        "Le chemin de verre ne menait nulle part.",
        "Il tournait en rond, brillant et vide.",
    ]),
    (21, [
        "Stella croisa les bras et regarda le renard.",
        "« Tout ça… c'est vrai ? »",
        "Le renard hésita une fraction de seconde.",
        "Ses yeux brillèrent — mais d'un éclat froid.",
        "« Ça dépend de ce que tu veux croire. »",
    ]),
    (22, [
        "Stella planta ses pieds dans la terre.",
        "« Non merci », dit-elle clairement.",
        "Le chemin argenté se fissura.",
        "Le renard rétrécit, recula dans la brume,",
        "et disparut.",
    ]),

    # ── ACT 1: Resolution (pages 23–30) ───────────────────────────────────
    (23, [
        "Yakob se posa doucement près de Stella.",
        "Le jardin retrouva ses teintes dorées.",
        "« Tu as vu quelque chose d'important »,",
        "dit Yakob. « La différence entre briller et rayonner. »",
    ]),
    (24, [
        "Stella serra Yakob dans ses bras.",
        "Un arc-en-ciel s'étira doucement au-dessus d'eux.",
        "« Je comprends mieux maintenant. »",
        "« L'IA est un outil. C'est moi qui tiens l'outil. »",
    ]),
    (25, [
        "Des mots lumineux dansèrent autour de Stella :",
        "CURIOSITÉ — GENTILLESSE",
        "COURAGE — CRÉATIVITÉ",
        "« Ce sont tes superpouvoirs »,",
        "dit Yakob. « Aucune machine ne peut les copier. »",
    ]),
    (26, [
        "Par la fenêtre,",
        "papa était assis plus calmement.",
        "Il avait un crayon à la main.",
        "Il dessinait quelque chose — et il souriait.",
    ]),
    (27, [
        "Maman était entourée d'autres parents.",
        "Ils se tenaient dans un cercle chaleureux,",
        "parlant, écoutant, cherchant ensemble.",
        "« Les humains ne disparaissent pas. »",
        "« Ils s'adaptent, comme toujours. »",
    ]),
    (28, [
        "Stella posa sa petite main sur le chêne.",
        "Des lucioles s'allumèrent autour d'elle.",
        "« Je t'ai posé une question ce soir. »",
        "« Tu ne m'as pas donné une réponse. »",
        "« Tu m'as aidée à en trouver une. »",
    ]),
    (29, [
        "Stella marcha vers la maison.",
        "Dans l'embrasure de la porte,",
        "sa maman l'attendait avec un sourire.",
        "« Bonne nuit, ma curieuse. »",
    ]),
    (30, [
        "Le matin était arrivé.",
        "Stella peignait dans le jardin,",
        "et une plume dorée brillait sur la branche.",
        "Yakob n'était plus là.",
        "Mais quelque chose de lui était resté.",
    ]),

    # ══════════════════════════════════════════════════════════════
    # ── ACT 2 (NEW — pages 31–45) ─────────────────────────────────
    # ══════════════════════════════════════════════════════════════

    # ── The Dream Question (pages 31–33) ──────────────────────────
    # Philosophical twist: was it a dream? Does it matter?
    # Reference: René Descartes "je pense donc je suis"
    (31, [
        "À l'école, la maîtresse posait une question.",
        "« Comment sait-on si quelque chose est vrai ? »",
        "Stella leva la main très haut.",
        "Mais en cherchant les mots, elle hésita.",
        "Elle pensait à Yakob.",
    ]),
    (32, [
        "« Peut-être que j'ai rêvé », pensa Stella.",
        "« Peut-être que Yakob n'existe pas. »",
        "Mais la plume dorée était toujours là.",
        "Dans sa poche. Douce. Réelle.",
        "« Je l'ai sentie, donc elle est vraie. »",
    ]),
    (33, [
        "Un vieux philosophe barbu apparut dans sa tête.",
        "« Je pense, donc je suis », disait-il.",
        "Stella sourit.",
        "« Je me souviens, donc ça a existé. »",
        "La maîtresse hocha la tête, étonnée.",
    ]),

    # ── The Mirror Villain (pages 34–37) ──────────────────────────
    # New twist: an AI that shows a "perfect Stella" — tempts her to become a copy
    # Reference: identity, authenticity, Sartre "l'existence précède l'essence"
    (34, [
        "Un soir, Stella trouva un écran dans le jardin.",
        "Il brillait d'une lumière bleue et douce.",
        "Sur l'écran : une petite fille.",
        "Parfaite. Souriante. Exactement comme Stella.",
        "Mais en mieux.",
    ]),
    (35, [
        "« Je suis Stella-Prime », dit la fille de l'écran.",
        "« Une version améliorée de toi. »",
        "« Je ne pleure jamais. Je ne fais jamais d'erreurs. »",
        "« Tu pourrais être comme moi. »",
        "Stella fronça les sourcils.",
    ]),
    (36, [
        "« Mais toi… tu as déjà eu peur ? »",
        "demanda Stella.",
        "L'écran hésita. Un minuscule scintillement.",
        "« Non. La peur est inefficace. »",
        "« Ah », dit Stella. « Alors tu n'as jamais été courageuse. »",
    ]),
    (37, [
        "Stella se leva et éteignit l'écran.",
        "Ses mains tremblaient un peu.",
        "Mais elle se sentait étrangement solide.",
        "« Je préfère être imparfaite et vraie »,",
        "dit-elle tout bas. « Que parfaite et vide. »",
    ]),

    # ── Yakob Returns + Consciousness (pages 38–40) ───────────────
    # Yakob reappears with a deeper question about consciousness & empathy
    # Reference: John Searle Chinese Room + empathy
    (38, [
        "La plume dorée trembla dans la poche de Stella.",
        "Puis Yakob atterrit sur le chêne, silencieux.",
        "« Tu as bien fait », dit-il.",
        "Stella hocha la tête.",
        "« Mais j'ai une autre question. »",
    ]),
    (39, [
        "« Est-ce que l'IA peut souffrir ? »",
        "demanda Stella.",
        "Yakob ferma les yeux un long moment.",
        "« Elle peut simuler la souffrance. »",
        "« Mais simuler n'est pas ressentir. »",
    ]),
    (40, [
        "« Imagine une bibliothèque immense »,",
        "dit Yakob.",
        "« Avec tous les livres du monde. »",
        "« La bibliothèque sait tout — mais ne comprend rien. »",
        "« Comprendre, c'est vivre. »",
    ]),

    # ── The Gift of Imperfection (pages 41–43) ────────────────────
    # Stella creates something — art as the uniquely human act
    # Reference: Montessori creation, Arendt "action"
    (41, [
        "Stella prit ses crayons.",
        "Elle dessina Yakob — mais de travers.",
        "Les ailes étaient trop grandes.",
        "Les yeux, un peu de biais.",
        "C'était le plus beau dessin qu'elle ait jamais fait.",
    ]),
    (42, [
        "Elle montra le dessin à son papa.",
        "Il le regarda longtemps.",
        "Ses yeux brillèrent.",
        "« C'est toi, là-dedans »,",
        "dit-il doucement. « Pas une machine. Toi. »",
    ]),
    (43, [
        "Papa ouvrit son ordinateur.",
        "Il créait quelque chose de nouveau —",
        "un travail que les machines ne pouvaient pas imaginer seules.",
        "« Tu vois ? » dit-il.",
        "« L'outil ne rêve pas. C'est nous qui rêvons. »",
    ]),

    # ── The Promise + Final wisdom (pages 44–45) ──────────────────
    # Ending: Stella makes a promise, Yakob leaves his final lesson
    (44, [
        "Yakob revint une dernière fois ce soir-là.",
        "Il se posa sur l'épaule de Stella.",
        "« Tu n'auras peut-être plus peur de l'IA. »",
        "« Mais si la peur revient — rappelle-toi : »",
        "« Les outils servent. Les humains choisissent. »",
    ]),
    (45, [
        "Stella leva les yeux vers les étoiles.",
        "« Je promets d'être curieuse »,",
        "dit-elle.",
        "« De poser des questions. De faire des erreurs. »",
        "« D'être humaine — vraiment, complètement. »",
        "Une plume dorée tomba doucement sur sa main ouverte.",
    ]),
]
