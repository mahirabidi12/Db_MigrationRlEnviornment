"""Task 1 (Easy): Acme Corp Acquired by GlobalTech — Blog Platform Migration.

Acme Corp ran a blog platform with its own schema conventions (acme_ prefix,
email-based references, denormalized columns). GlobalTech acquired Acme and
needs the data migrated into GlobalTech's standardized schema with proper
FK relationships, constraints, and normalized tables.

ZERO table name overlap between initial and target schemas.

Initial: 10 tables (acme_* prefix), ~68 rows total, email-based references
Target:  15 tables (GlobalTech standard names), proper FKs, constraints,
         5 new tables (user_profiles, activity_log, bookmarks, post_stats, notifications)

Skills tested: DROP/CREATE with new names, INSERT...SELECT with JOINs to
resolve email→id, splitting tables, creating computed aggregates, data
transformation across completely different schemas.
"""

TASK_ID = "easy_blog_acquisition"
TASK_DESCRIPTION = (
    "Acme Corp was acquired by GlobalTech. Migrate the Acme blog platform database "
    "(10 acme_* tables with email-based references) into GlobalTech's standard schema "
    "(15 tables with completely different names, proper integer FKs, NOT NULL/UNIQUE "
    "constraints). Split acme_users into users + user_profiles. Resolve all email/name "
    "references to integer FK IDs. Create activity_log, bookmarks, post_stats, and "
    "notifications tables. Preserve all data with referential integrity."
)
DIFFICULTY = "easy"
TIMEOUT_SECONDS = 1800  # 30 minutes

INITIAL_SQL = """
CREATE TABLE acme_users (
    usr_id INTEGER PRIMARY KEY,
    usr_name TEXT,
    usr_email TEXT,
    usr_pass TEXT,
    usr_fullname TEXT,
    usr_bio TEXT,
    usr_avatar TEXT,
    usr_phone TEXT,
    usr_city TEXT,
    usr_state TEXT,
    usr_country TEXT,
    created TEXT
);
INSERT INTO acme_users VALUES (1,'alice','alice@acme.com','h1','Alice Johnson','Tech blogger','https://img.co/alice.jpg','555-0101','Austin','TX','US','2024-01-01');
INSERT INTO acme_users VALUES (2,'bob','bob@acme.com','h2','Bob Smith','Travel writer','https://img.co/bob.jpg','555-0202','Portland','OR','US','2024-01-15');
INSERT INTO acme_users VALUES (3,'carol','carol@acme.com','h3','Carol Lee','Food critic','https://img.co/carol.jpg','555-0303','Chicago','IL','US','2024-02-01');
INSERT INTO acme_users VALUES (4,'dave','dave@acme.com','h4','Dave Brown','Sports analyst','https://img.co/dave.jpg','555-0404','Miami','FL','US','2024-02-10');
INSERT INTO acme_users VALUES (5,'eve','eve@acme.com','h5','Eve Martinez','Science editor','https://img.co/eve.jpg','555-0505','Denver','CO','US','2024-03-01');
INSERT INTO acme_users VALUES (6,'frank','frank@acme.com','h6','Frank Wilson','Music reviewer',NULL,'555-0606','Seattle','WA','US','2024-03-15');

CREATE TABLE acme_cats (
    cat_id INTEGER PRIMARY KEY,
    cat_name TEXT,
    cat_slug TEXT,
    cat_desc TEXT,
    cat_parent TEXT,
    cat_posts INTEGER,
    cat_active INTEGER,
    cat_icon TEXT,
    cat_sort INTEGER,
    cat_created TEXT
);
INSERT INTO acme_cats VALUES (1,'Technology','technology','All things tech',NULL,3,1,'icon-tech.png',1,'2024-01-01');
INSERT INTO acme_cats VALUES (2,'Travel','travel','Travel stories',NULL,2,1,'icon-travel.png',2,'2024-01-01');
INSERT INTO acme_cats VALUES (3,'Food','food','Recipes and reviews',NULL,2,1,'icon-food.png',3,'2024-01-01');
INSERT INTO acme_cats VALUES (4,'Web Dev','web-dev','Web development','Technology',1,1,'icon-webdev.png',4,'2024-01-05');
INSERT INTO acme_cats VALUES (5,'AI/ML','ai-ml','Artificial intelligence','Technology',1,1,'icon-ai.png',5,'2024-01-10');

CREATE TABLE acme_articles (
    art_id INTEGER PRIMARY KEY,
    art_author_email TEXT,
    art_title TEXT,
    art_slug TEXT,
    art_body TEXT,
    art_excerpt TEXT,
    art_cat_name TEXT,
    art_img TEXT,
    art_published INTEGER,
    art_views INTEGER,
    art_created TEXT,
    art_updated TEXT
);
INSERT INTO acme_articles VALUES (1,'alice@acme.com','Getting Started with Python','python-start','Python is great...','Intro to Python','Technology','img1.jpg',1,1200,'2024-01-10','2024-01-10');
INSERT INTO acme_articles VALUES (2,'bob@acme.com','Hiking in Oregon','oregon-hiking','The trails are...','Oregon trails','Travel','img2.jpg',1,800,'2024-01-20','2024-01-22');
INSERT INTO acme_articles VALUES (3,'carol@acme.com','Best Tacos in Chicago','chicago-tacos','If you love tacos...','Taco tour','Food','img3.jpg',1,950,'2024-02-05','2024-02-05');
INSERT INTO acme_articles VALUES (4,'alice@acme.com','React vs Vue in 2024','react-vue','Comparing frameworks...','Framework comparison','Web Dev','img4.jpg',1,2100,'2024-02-15','2024-02-20');
INSERT INTO acme_articles VALUES (5,'eve@acme.com','Introduction to LLMs','intro-llms','Large language models...','LLM basics','AI/ML','img5.jpg',1,3200,'2024-03-01','2024-03-05');
INSERT INTO acme_articles VALUES (6,'bob@acme.com','Budget Travel Tips','budget-travel','Save money while...','Budget tips','Travel','img6.jpg',1,600,'2024-03-10','2024-03-10');
INSERT INTO acme_articles VALUES (7,'carol@acme.com','Homemade Pasta Guide','pasta-guide','Making pasta from...','Pasta tutorial','Food','img7.jpg',0,0,'2024-03-15',NULL);

CREATE TABLE acme_replies (
    rpl_id INTEGER PRIMARY KEY,
    rpl_art_id INTEGER,
    rpl_email TEXT,
    rpl_name TEXT,
    rpl_body TEXT,
    rpl_approved INTEGER,
    rpl_parent INTEGER,
    rpl_ip TEXT,
    rpl_likes INTEGER,
    rpl_created TEXT
);
INSERT INTO acme_replies VALUES (1,1,'bob@acme.com','Bob Smith','Great tutorial!',1,NULL,'10.0.0.1',5,'2024-01-11');
INSERT INTO acme_replies VALUES (2,1,'carol@acme.com','Carol Lee','Very helpful',1,NULL,'10.0.0.2',3,'2024-01-12');
INSERT INTO acme_replies VALUES (3,1,'bob@acme.com','Bob Smith','Thanks for the update',1,1,'10.0.0.1',1,'2024-01-13');
INSERT INTO acme_replies VALUES (4,3,'alice@acme.com','Alice Johnson','I agree!',1,NULL,'10.0.0.3',2,'2024-02-06');
INSERT INTO acme_replies VALUES (5,5,'dave@acme.com','Dave Brown','Fascinating read',1,NULL,'10.0.0.4',8,'2024-03-02');
INSERT INTO acme_replies VALUES (6,5,'frank@acme.com','Frank Wilson','Need more examples',0,NULL,'10.0.0.5',0,'2024-03-03');
INSERT INTO acme_replies VALUES (7,4,'eve@acme.com','Eve Martinez','Vue is better IMO',1,NULL,'10.0.0.6',4,'2024-02-16');
INSERT INTO acme_replies VALUES (8,2,'carol@acme.com','Carol Lee','Beautiful photos!',1,NULL,'10.0.0.2',2,'2024-01-21');

CREATE TABLE acme_labels (
    lbl_id INTEGER PRIMARY KEY,
    lbl_name TEXT,
    lbl_slug TEXT,
    lbl_desc TEXT,
    lbl_count INTEGER,
    lbl_trending INTEGER,
    lbl_color TEXT,
    lbl_creator_email TEXT,
    lbl_icon TEXT,
    lbl_created TEXT
);
INSERT INTO acme_labels VALUES (1,'python','python','Python programming',3,1,'#3776AB','alice@acme.com','py-icon','2024-01-01');
INSERT INTO acme_labels VALUES (2,'travel','travel','Travel content',2,0,'#2ECC71','bob@acme.com','travel-icon','2024-01-01');
INSERT INTO acme_labels VALUES (3,'food','food','Food content',2,0,'#E74C3C','carol@acme.com','food-icon','2024-01-01');
INSERT INTO acme_labels VALUES (4,'javascript','javascript','JS programming',2,1,'#F7DF1E','alice@acme.com','js-icon','2024-01-05');
INSERT INTO acme_labels VALUES (5,'ai','ai','Artificial intelligence',1,1,'#9B59B6','eve@acme.com','ai-icon','2024-02-01');
INSERT INTO acme_labels VALUES (6,'tutorial','tutorial','How-to guides',4,0,'#1ABC9C','alice@acme.com','tut-icon','2024-01-01');

CREATE TABLE acme_art_labels (
    al_id INTEGER PRIMARY KEY,
    al_art_id INTEGER,
    al_label_name TEXT,
    al_added_by_email TEXT,
    al_added_at TEXT,
    al_primary INTEGER,
    al_weight REAL,
    al_source TEXT,
    al_auto INTEGER,
    al_score REAL
);
INSERT INTO acme_art_labels VALUES (1,1,'python','alice@acme.com','2024-01-10',1,1.0,'manual',0,0.95);
INSERT INTO acme_art_labels VALUES (2,1,'tutorial','alice@acme.com','2024-01-10',0,0.8,'manual',0,0.85);
INSERT INTO acme_art_labels VALUES (3,2,'travel','bob@acme.com','2024-01-20',1,1.0,'manual',0,0.90);
INSERT INTO acme_art_labels VALUES (4,3,'food','carol@acme.com','2024-02-05',1,1.0,'manual',0,0.95);
INSERT INTO acme_art_labels VALUES (5,4,'javascript','alice@acme.com','2024-02-15',1,1.0,'manual',0,0.90);
INSERT INTO acme_art_labels VALUES (6,4,'tutorial','alice@acme.com','2024-02-15',0,0.7,'auto',1,0.75);
INSERT INTO acme_art_labels VALUES (7,5,'ai','eve@acme.com','2024-03-01',1,1.0,'manual',0,0.98);
INSERT INTO acme_art_labels VALUES (8,5,'python','eve@acme.com','2024-03-01',0,0.6,'auto',1,0.70);
INSERT INTO acme_art_labels VALUES (9,5,'tutorial','eve@acme.com','2024-03-01',0,0.5,'auto',1,0.65);
INSERT INTO acme_art_labels VALUES (10,6,'travel','bob@acme.com','2024-03-10',1,1.0,'manual',0,0.88);
INSERT INTO acme_art_labels VALUES (11,3,'tutorial','carol@acme.com','2024-02-05',0,0.6,'auto',1,0.60);

CREATE TABLE acme_reactions (
    rxn_id INTEGER PRIMARY KEY,
    rxn_art_id INTEGER,
    rxn_user_email TEXT,
    rxn_type TEXT,
    rxn_at TEXT,
    rxn_ip TEXT,
    rxn_ua TEXT,
    rxn_counted INTEGER,
    rxn_page TEXT,
    rxn_session TEXT
);
INSERT INTO acme_reactions VALUES (1,1,'bob@acme.com','like','2024-01-11','10.0.0.1','Mozilla/5.0',1,'/post/1','s001');
INSERT INTO acme_reactions VALUES (2,1,'carol@acme.com','love','2024-01-12','10.0.0.2','Chrome/120',1,'/post/1','s002');
INSERT INTO acme_reactions VALUES (3,5,'alice@acme.com','like','2024-03-02','10.0.0.3','Safari/17',1,'/post/5','s003');
INSERT INTO acme_reactions VALUES (4,5,'bob@acme.com','love','2024-03-02','10.0.0.1','Mozilla/5.0',1,'/post/5','s004');
INSERT INTO acme_reactions VALUES (5,4,'eve@acme.com','like','2024-02-16','10.0.0.6','Chrome/120',1,'/post/4','s005');
INSERT INTO acme_reactions VALUES (6,3,'dave@acme.com','like','2024-02-06','10.0.0.4','Safari/17',1,'/post/3','s006');
INSERT INTO acme_reactions VALUES (7,5,'dave@acme.com','like','2024-03-03','10.0.0.4','Safari/17',1,'/feed','s007');

CREATE TABLE acme_follows (
    flw_id INTEGER PRIMARY KEY,
    flw_follower_email TEXT,
    flw_following_email TEXT,
    flw_at TEXT,
    flw_mutual INTEGER,
    flw_notify INTEGER,
    flw_source TEXT,
    flw_blocked INTEGER,
    flw_muted INTEGER,
    flw_notes TEXT
);
INSERT INTO acme_follows VALUES (1,'bob@acme.com','alice@acme.com','2024-01-15',1,1,'profile',0,0,NULL);
INSERT INTO acme_follows VALUES (2,'alice@acme.com','bob@acme.com','2024-01-16',1,1,'suggestion',0,0,NULL);
INSERT INTO acme_follows VALUES (3,'carol@acme.com','alice@acme.com','2024-02-01',0,1,'profile',0,0,NULL);
INSERT INTO acme_follows VALUES (4,'dave@acme.com','eve@acme.com','2024-03-01',0,1,'post',0,0,NULL);
INSERT INTO acme_follows VALUES (5,'eve@acme.com','alice@acme.com','2024-03-02',0,0,'search',0,0,NULL);
INSERT INTO acme_follows VALUES (6,'frank@acme.com','bob@acme.com','2024-03-15',0,1,'profile',0,0,NULL);

CREATE TABLE acme_uploads (
    upl_id INTEGER PRIMARY KEY,
    upl_file TEXT,
    upl_url TEXT,
    upl_mime TEXT,
    upl_size INTEGER,
    upl_w INTEGER,
    upl_h INTEGER,
    upl_by_email TEXT,
    upl_art_id INTEGER,
    upl_alt TEXT,
    upl_created TEXT
);
INSERT INTO acme_uploads VALUES (1,'img1.jpg','https://cdn.blog.com/img1.jpg','image/jpeg',245000,1920,1080,'alice@acme.com',1,'Python code screenshot','2024-01-10');
INSERT INTO acme_uploads VALUES (2,'img2.jpg','https://cdn.blog.com/img2.jpg','image/jpeg',380000,2400,1600,'bob@acme.com',2,'Oregon trail photo','2024-01-20');
INSERT INTO acme_uploads VALUES (3,'img3.jpg','https://cdn.blog.com/img3.jpg','image/jpeg',195000,1600,1200,'carol@acme.com',3,'Chicago tacos','2024-02-05');
INSERT INTO acme_uploads VALUES (4,'img4.jpg','https://cdn.blog.com/img4.jpg','image/png',120000,1200,800,'alice@acme.com',4,'Framework comparison chart','2024-02-15');
INSERT INTO acme_uploads VALUES (5,'img5.jpg','https://cdn.blog.com/img5.jpg','image/jpeg',290000,1920,1080,'eve@acme.com',5,'Neural network diagram','2024-03-01');
INSERT INTO acme_uploads VALUES (6,'avatar-frank.jpg','https://cdn.blog.com/avatars/frank.jpg','image/jpeg',45000,400,400,'frank@acme.com',NULL,'Frank profile photo','2024-03-15');

CREATE TABLE acme_prefs (
    prf_id INTEGER PRIMARY KEY,
    prf_user_email TEXT,
    prf_theme TEXT,
    prf_lang TEXT,
    prf_tz TEXT,
    prf_email_notif INTEGER,
    prf_push_notif INTEGER,
    prf_privacy TEXT,
    prf_2fa INTEGER,
    prf_last_login TEXT,
    prf_logins INTEGER
);
INSERT INTO acme_prefs VALUES (1,'alice@acme.com','dark','en','America/Chicago',1,1,'public',1,'2024-03-20',145);
INSERT INTO acme_prefs VALUES (2,'bob@acme.com','light','en','America/Los_Angeles',1,0,'public',0,'2024-03-18',89);
INSERT INTO acme_prefs VALUES (3,'carol@acme.com','dark','en','America/Chicago',1,1,'friends',0,'2024-03-19',112);
INSERT INTO acme_prefs VALUES (4,'dave@acme.com','light','en','America/New_York',0,0,'public',0,'2024-03-15',34);
INSERT INTO acme_prefs VALUES (5,'eve@acme.com','dark','en','America/Denver',1,1,'private',1,'2024-03-20',167);
INSERT INTO acme_prefs VALUES (6,'frank@acme.com','light','en','America/Los_Angeles',1,0,'public',0,'2024-03-16',12);
"""

TARGET_SQL = """
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    created_at TEXT NOT NULL
);
INSERT INTO users VALUES (1,'alice','alice@acme.com','h1','Alice Johnson','2024-01-01');
INSERT INTO users VALUES (2,'bob','bob@acme.com','h2','Bob Smith','2024-01-15');
INSERT INTO users VALUES (3,'carol','carol@acme.com','h3','Carol Lee','2024-02-01');
INSERT INTO users VALUES (4,'dave','dave@acme.com','h4','Dave Brown','2024-02-10');
INSERT INTO users VALUES (5,'eve','eve@acme.com','h5','Eve Martinez','2024-03-01');
INSERT INTO users VALUES (6,'frank','frank@acme.com','h6','Frank Wilson','2024-03-15');

CREATE TABLE user_profiles (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    bio TEXT,
    avatar_url TEXT,
    phone TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
INSERT INTO user_profiles VALUES (1,1,'Tech blogger','https://img.co/alice.jpg','555-0101','Austin','TX','US');
INSERT INTO user_profiles VALUES (2,2,'Travel writer','https://img.co/bob.jpg','555-0202','Portland','OR','US');
INSERT INTO user_profiles VALUES (3,3,'Food critic','https://img.co/carol.jpg','555-0303','Chicago','IL','US');
INSERT INTO user_profiles VALUES (4,4,'Sports analyst','https://img.co/dave.jpg','555-0404','Miami','FL','US');
INSERT INTO user_profiles VALUES (5,5,'Science editor','https://img.co/eve.jpg','555-0505','Denver','CO','US');
INSERT INTO user_profiles VALUES (6,6,'Music reviewer',NULL,'555-0606','Seattle','WA','US');

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    parent_id INTEGER,
    is_active INTEGER NOT NULL DEFAULT 1,
    icon_url TEXT,
    sort_order INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);
INSERT INTO categories VALUES (1,'Technology','technology','All things tech',NULL,1,'icon-tech.png',1,'2024-01-01');
INSERT INTO categories VALUES (2,'Travel','travel','Travel stories',NULL,1,'icon-travel.png',2,'2024-01-01');
INSERT INTO categories VALUES (3,'Food','food','Recipes and reviews',NULL,1,'icon-food.png',3,'2024-01-01');
INSERT INTO categories VALUES (4,'Web Dev','web-dev','Web development',1,1,'icon-webdev.png',4,'2024-01-05');
INSERT INTO categories VALUES (5,'AI/ML','ai-ml','Artificial intelligence',1,1,'icon-ai.png',5,'2024-01-10');

CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    author_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    body TEXT NOT NULL,
    excerpt TEXT,
    category_id INTEGER NOT NULL,
    image_url TEXT,
    is_published INTEGER NOT NULL DEFAULT 0,
    view_count INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT,
    FOREIGN KEY (author_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
INSERT INTO posts VALUES (1,1,'Getting Started with Python','python-start','Python is great...','Intro to Python',1,'img1.jpg',1,1200,'2024-01-10','2024-01-10');
INSERT INTO posts VALUES (2,2,'Hiking in Oregon','oregon-hiking','The trails are...','Oregon trails',2,'img2.jpg',1,800,'2024-01-20','2024-01-22');
INSERT INTO posts VALUES (3,3,'Best Tacos in Chicago','chicago-tacos','If you love tacos...','Taco tour',3,'img3.jpg',1,950,'2024-02-05','2024-02-05');
INSERT INTO posts VALUES (4,1,'React vs Vue in 2024','react-vue','Comparing frameworks...','Framework comparison',4,'img4.jpg',1,2100,'2024-02-15','2024-02-20');
INSERT INTO posts VALUES (5,5,'Introduction to LLMs','intro-llms','Large language models...','LLM basics',5,'img5.jpg',1,3200,'2024-03-01','2024-03-05');
INSERT INTO posts VALUES (6,2,'Budget Travel Tips','budget-travel','Save money while...','Budget tips',2,'img6.jpg',1,600,'2024-03-10','2024-03-10');
INSERT INTO posts VALUES (7,3,'Homemade Pasta Guide','pasta-guide','Making pasta from...','Pasta tutorial',3,'img7.jpg',0,0,'2024-03-15',NULL);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    body TEXT NOT NULL,
    is_approved INTEGER NOT NULL DEFAULT 0,
    parent_comment_id INTEGER,
    ip_address TEXT,
    likes_count INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (parent_comment_id) REFERENCES comments(id)
);
INSERT INTO comments VALUES (1,1,2,'Great tutorial!',1,NULL,'10.0.0.1',5,'2024-01-11');
INSERT INTO comments VALUES (2,1,3,'Very helpful',1,NULL,'10.0.0.2',3,'2024-01-12');
INSERT INTO comments VALUES (3,1,2,'Thanks for the update',1,1,'10.0.0.1',1,'2024-01-13');
INSERT INTO comments VALUES (4,3,1,'I agree!',1,NULL,'10.0.0.3',2,'2024-02-06');
INSERT INTO comments VALUES (5,5,4,'Fascinating read',1,NULL,'10.0.0.4',8,'2024-03-02');
INSERT INTO comments VALUES (6,5,6,'Need more examples',0,NULL,'10.0.0.5',0,'2024-03-03');
INSERT INTO comments VALUES (7,4,5,'Vue is better IMO',1,NULL,'10.0.0.6',4,'2024-02-16');
INSERT INTO comments VALUES (8,2,3,'Beautiful photos!',1,NULL,'10.0.0.2',2,'2024-01-21');

CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    usage_count INTEGER NOT NULL DEFAULT 0,
    is_trending INTEGER NOT NULL DEFAULT 0,
    color TEXT,
    created_by_id INTEGER NOT NULL,
    icon TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (created_by_id) REFERENCES users(id)
);
INSERT INTO tags VALUES (1,'python','python','Python programming',3,1,'#3776AB',1,'py-icon','2024-01-01');
INSERT INTO tags VALUES (2,'travel','travel','Travel content',2,0,'#2ECC71',2,'travel-icon','2024-01-01');
INSERT INTO tags VALUES (3,'food','food','Food content',2,0,'#E74C3C',3,'food-icon','2024-01-01');
INSERT INTO tags VALUES (4,'javascript','javascript','JS programming',2,1,'#F7DF1E',1,'js-icon','2024-01-05');
INSERT INTO tags VALUES (5,'ai','ai','Artificial intelligence',1,1,'#9B59B6',5,'ai-icon','2024-02-01');
INSERT INTO tags VALUES (6,'tutorial','tutorial','How-to guides',4,0,'#1ABC9C',1,'tut-icon','2024-01-01');

CREATE TABLE post_tags (
    id INTEGER PRIMARY KEY,
    post_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    added_by_id INTEGER NOT NULL,
    added_at TEXT NOT NULL,
    is_primary INTEGER NOT NULL DEFAULT 0,
    weight REAL NOT NULL DEFAULT 1.0,
    source TEXT NOT NULL DEFAULT 'manual',
    auto_tagged INTEGER NOT NULL DEFAULT 0,
    relevance_score REAL,
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id),
    FOREIGN KEY (added_by_id) REFERENCES users(id)
);
INSERT INTO post_tags VALUES (1,1,1,1,'2024-01-10',1,1.0,'manual',0,0.95);
INSERT INTO post_tags VALUES (2,1,6,1,'2024-01-10',0,0.8,'manual',0,0.85);
INSERT INTO post_tags VALUES (3,2,2,2,'2024-01-20',1,1.0,'manual',0,0.90);
INSERT INTO post_tags VALUES (4,3,3,3,'2024-02-05',1,1.0,'manual',0,0.95);
INSERT INTO post_tags VALUES (5,4,4,1,'2024-02-15',1,1.0,'manual',0,0.90);
INSERT INTO post_tags VALUES (6,4,6,1,'2024-02-15',0,0.7,'auto',1,0.75);
INSERT INTO post_tags VALUES (7,5,5,5,'2024-03-01',1,1.0,'manual',0,0.98);
INSERT INTO post_tags VALUES (8,5,1,5,'2024-03-01',0,0.6,'auto',1,0.70);
INSERT INTO post_tags VALUES (9,5,6,5,'2024-03-01',0,0.5,'auto',1,0.65);
INSERT INTO post_tags VALUES (10,6,2,2,'2024-03-10',1,1.0,'manual',0,0.88);
INSERT INTO post_tags VALUES (11,3,6,3,'2024-02-05',0,0.6,'auto',1,0.60);

CREATE TABLE likes (
    id INTEGER PRIMARY KEY,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    reaction_type TEXT NOT NULL DEFAULT 'like',
    liked_at TEXT NOT NULL,
    ip_address TEXT,
    user_agent TEXT,
    is_counted INTEGER NOT NULL DEFAULT 1,
    source_page TEXT,
    session_id TEXT,
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
INSERT INTO likes VALUES (1,1,2,'like','2024-01-11','10.0.0.1','Mozilla/5.0',1,'/post/1','s001');
INSERT INTO likes VALUES (2,1,3,'love','2024-01-12','10.0.0.2','Chrome/120',1,'/post/1','s002');
INSERT INTO likes VALUES (3,5,1,'like','2024-03-02','10.0.0.3','Safari/17',1,'/post/5','s003');
INSERT INTO likes VALUES (4,5,2,'love','2024-03-02','10.0.0.1','Mozilla/5.0',1,'/post/5','s004');
INSERT INTO likes VALUES (5,4,5,'like','2024-02-16','10.0.0.6','Chrome/120',1,'/post/4','s005');
INSERT INTO likes VALUES (6,3,4,'like','2024-02-06','10.0.0.4','Safari/17',1,'/post/3','s006');
INSERT INTO likes VALUES (7,5,4,'like','2024-03-03','10.0.0.4','Safari/17',1,'/feed','s007');

CREATE TABLE followers (
    id INTEGER PRIMARY KEY,
    follower_id INTEGER NOT NULL,
    following_id INTEGER NOT NULL,
    followed_at TEXT NOT NULL,
    is_mutual INTEGER NOT NULL DEFAULT 0,
    notifications_on INTEGER NOT NULL DEFAULT 1,
    source TEXT,
    is_blocked INTEGER NOT NULL DEFAULT 0,
    is_muted INTEGER NOT NULL DEFAULT 0,
    notes TEXT,
    FOREIGN KEY (follower_id) REFERENCES users(id),
    FOREIGN KEY (following_id) REFERENCES users(id)
);
INSERT INTO followers VALUES (1,2,1,'2024-01-15',1,1,'profile',0,0,NULL);
INSERT INTO followers VALUES (2,1,2,'2024-01-16',1,1,'suggestion',0,0,NULL);
INSERT INTO followers VALUES (3,3,1,'2024-02-01',0,1,'profile',0,0,NULL);
INSERT INTO followers VALUES (4,4,5,'2024-03-01',0,1,'post',0,0,NULL);
INSERT INTO followers VALUES (5,5,1,'2024-03-02',0,0,'search',0,0,NULL);
INSERT INTO followers VALUES (6,6,2,'2024-03-15',0,1,'profile',0,0,NULL);

CREATE TABLE media (
    id INTEGER PRIMARY KEY,
    filename TEXT NOT NULL,
    url TEXT NOT NULL,
    mime_type TEXT NOT NULL,
    size_bytes INTEGER NOT NULL,
    width INTEGER,
    height INTEGER,
    uploader_id INTEGER NOT NULL,
    post_id INTEGER,
    alt_text TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (uploader_id) REFERENCES users(id),
    FOREIGN KEY (post_id) REFERENCES posts(id)
);
INSERT INTO media VALUES (1,'img1.jpg','https://cdn.blog.com/img1.jpg','image/jpeg',245000,1920,1080,1,1,'Python code screenshot','2024-01-10');
INSERT INTO media VALUES (2,'img2.jpg','https://cdn.blog.com/img2.jpg','image/jpeg',380000,2400,1600,2,2,'Oregon trail photo','2024-01-20');
INSERT INTO media VALUES (3,'img3.jpg','https://cdn.blog.com/img3.jpg','image/jpeg',195000,1600,1200,3,3,'Chicago tacos','2024-02-05');
INSERT INTO media VALUES (4,'img4.jpg','https://cdn.blog.com/img4.jpg','image/png',120000,1200,800,1,4,'Framework comparison chart','2024-02-15');
INSERT INTO media VALUES (5,'img5.jpg','https://cdn.blog.com/img5.jpg','image/jpeg',290000,1920,1080,5,5,'Neural network diagram','2024-03-01');
INSERT INTO media VALUES (6,'avatar-frank.jpg','https://cdn.blog.com/avatars/frank.jpg','image/jpeg',45000,400,400,6,NULL,'Frank profile photo','2024-03-15');

CREATE TABLE settings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    theme TEXT NOT NULL DEFAULT 'light',
    language TEXT NOT NULL DEFAULT 'en',
    timezone TEXT NOT NULL DEFAULT 'UTC',
    email_notifications INTEGER NOT NULL DEFAULT 1,
    push_notifications INTEGER NOT NULL DEFAULT 0,
    privacy_level TEXT NOT NULL DEFAULT 'public',
    two_factor_enabled INTEGER NOT NULL DEFAULT 0,
    last_login TEXT,
    login_count INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
INSERT INTO settings VALUES (1,1,'dark','en','America/Chicago',1,1,'public',1,'2024-03-20',145);
INSERT INTO settings VALUES (2,2,'light','en','America/Los_Angeles',1,0,'public',0,'2024-03-18',89);
INSERT INTO settings VALUES (3,3,'dark','en','America/Chicago',1,1,'friends',0,'2024-03-19',112);
INSERT INTO settings VALUES (4,4,'light','en','America/New_York',0,0,'public',0,'2024-03-15',34);
INSERT INTO settings VALUES (5,5,'dark','en','America/Denver',1,1,'private',1,'2024-03-20',167);
INSERT INTO settings VALUES (6,6,'light','en','America/Los_Angeles',1,0,'public',0,'2024-03-16',12);

CREATE TABLE activity_log (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
INSERT INTO activity_log VALUES (1,1,'migrated','2024-03-20');
INSERT INTO activity_log VALUES (2,2,'migrated','2024-03-20');
INSERT INTO activity_log VALUES (3,3,'migrated','2024-03-20');
INSERT INTO activity_log VALUES (4,4,'migrated','2024-03-20');
INSERT INTO activity_log VALUES (5,5,'migrated','2024-03-20');
INSERT INTO activity_log VALUES (6,6,'migrated','2024-03-20');

CREATE TABLE bookmarks (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    notes TEXT,
    is_private INTEGER NOT NULL DEFAULT 1,
    folder TEXT DEFAULT 'default',
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (post_id) REFERENCES posts(id)
);
INSERT INTO bookmarks VALUES (1,2,1,'2024-01-11',NULL,1,'default');
INSERT INTO bookmarks VALUES (2,3,5,'2024-03-02','Great AI article',0,'research');
INSERT INTO bookmarks VALUES (3,1,3,'2024-02-06',NULL,1,'food');
INSERT INTO bookmarks VALUES (4,5,4,'2024-02-16','Compare later',1,'dev');
INSERT INTO bookmarks VALUES (5,4,5,'2024-03-03',NULL,1,'default');

CREATE TABLE post_stats (
    id INTEGER PRIMARY KEY,
    post_id INTEGER NOT NULL UNIQUE,
    like_count INTEGER NOT NULL DEFAULT 0,
    comment_count INTEGER NOT NULL DEFAULT 0,
    bookmark_count INTEGER NOT NULL DEFAULT 0,
    avg_read_time_sec INTEGER,
    share_count INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (post_id) REFERENCES posts(id)
);
INSERT INTO post_stats VALUES (1,1,2,3,1,180,0);
INSERT INTO post_stats VALUES (2,2,0,1,0,240,0);
INSERT INTO post_stats VALUES (3,3,1,1,1,150,0);
INSERT INTO post_stats VALUES (4,4,1,1,1,300,0);
INSERT INTO post_stats VALUES (5,5,3,2,2,420,0);
INSERT INTO post_stats VALUES (6,6,0,0,0,120,0);
INSERT INTO post_stats VALUES (7,7,0,0,0,NULL,0);

CREATE TABLE notifications (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    is_read INTEGER NOT NULL DEFAULT 0,
    source_user_id INTEGER,
    source_post_id INTEGER,
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (source_user_id) REFERENCES users(id),
    FOREIGN KEY (source_post_id) REFERENCES posts(id)
);
INSERT INTO notifications VALUES (1,1,'comment','New comment on your post','Bob commented on Getting Started with Python',0,2,1,'2024-01-11');
INSERT INTO notifications VALUES (2,1,'follow','New follower','Bob started following you',1,2,NULL,'2024-01-15');
INSERT INTO notifications VALUES (3,5,'comment','New comment on your post','Dave commented on Introduction to LLMs',0,4,5,'2024-03-02');
INSERT INTO notifications VALUES (4,1,'like','Post liked','Eve liked React vs Vue in 2024',1,5,4,'2024-02-16');
INSERT INTO notifications VALUES (5,3,'like','Post liked','Dave liked Best Tacos in Chicago',0,4,3,'2024-02-06');
"""
