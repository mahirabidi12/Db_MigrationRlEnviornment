"""Task 1 (Easy): Blog Platform — Fix FK References & Add Constraints.

A blogging platform with 10 tables where relationships are stored as
emails/names instead of proper FK IDs. The agent must replace text
references with integer FKs, add missing constraints, and create an
audit trail table.

Initial: 10 tables, ~60 rows total, denormalized references
Target:  15 tables, proper FKs everywhere, constraints, 5 new tables (user_profiles, activity_log, bookmarks, post_stats, notifications)

Skills tested: ALTER TABLE (SQLite recreate pattern), INSERT...SELECT with JOINs
to resolve email→id, creating new tables with FKs, data preservation.
"""

TASK_ID = "easy_blog_fix_fks"
TASK_DESCRIPTION = (
    "Fix the blog platform database: replace all email/name-based references with "
    "proper integer FK columns (user_id) by JOINing on the users table. "
    "Add NOT NULL and UNIQUE constraints where missing. "
    "Create a 'user_profiles' table (split bio/avatar/location from users). "
    "Create an 'activity_log' table with one 'migrated' entry per user. "
    "Preserve all data with referential integrity."
)
DIFFICULTY = "easy"
MAX_STEPS = 80

INITIAL_SQL = """
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    email TEXT,
    password_hash TEXT,
    full_name TEXT,
    bio TEXT,
    avatar_url TEXT,
    phone TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    created_at TEXT
);
INSERT INTO users VALUES (1,'alice','alice@blog.com','h1','Alice Johnson','Tech blogger','https://img.co/alice.jpg','555-0101','Austin','TX','US','2024-01-01');
INSERT INTO users VALUES (2,'bob','bob@blog.com','h2','Bob Smith','Travel writer','https://img.co/bob.jpg','555-0202','Portland','OR','US','2024-01-15');
INSERT INTO users VALUES (3,'carol','carol@blog.com','h3','Carol Lee','Food critic','https://img.co/carol.jpg','555-0303','Chicago','IL','US','2024-02-01');
INSERT INTO users VALUES (4,'dave','dave@blog.com','h4','Dave Brown','Sports analyst','https://img.co/dave.jpg','555-0404','Miami','FL','US','2024-02-10');
INSERT INTO users VALUES (5,'eve','eve@blog.com','h5','Eve Martinez','Science editor','https://img.co/eve.jpg','555-0505','Denver','CO','US','2024-03-01');
INSERT INTO users VALUES (6,'frank','frank@blog.com','h6','Frank Wilson','Music reviewer',NULL,'555-0606','Seattle','WA','US','2024-03-15');

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT,
    slug TEXT,
    description TEXT,
    parent_id INTEGER,
    post_count INTEGER,
    is_active INTEGER,
    icon_url TEXT,
    sort_order INTEGER,
    created_at TEXT
);
INSERT INTO categories VALUES (1,'Technology','technology','All things tech',NULL,3,1,'icon-tech.png',1,'2024-01-01');
INSERT INTO categories VALUES (2,'Travel','travel','Travel stories',NULL,2,1,'icon-travel.png',2,'2024-01-01');
INSERT INTO categories VALUES (3,'Food','food','Recipes and reviews',NULL,2,1,'icon-food.png',3,'2024-01-01');
INSERT INTO categories VALUES (4,'Web Dev','web-dev','Web development',1,1,1,'icon-webdev.png',4,'2024-01-05');
INSERT INTO categories VALUES (5,'AI/ML','ai-ml','Artificial intelligence',1,1,1,'icon-ai.png',5,'2024-01-10');

CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    author_email TEXT,
    title TEXT,
    slug TEXT,
    body TEXT,
    excerpt TEXT,
    category_name TEXT,
    image_url TEXT,
    is_published INTEGER,
    view_count INTEGER,
    created_at TEXT,
    updated_at TEXT
);
INSERT INTO posts VALUES (1,'alice@blog.com','Getting Started with Python','python-start','Python is great...','Intro to Python','Technology','img1.jpg',1,1200,'2024-01-10','2024-01-10');
INSERT INTO posts VALUES (2,'bob@blog.com','Hiking in Oregon','oregon-hiking','The trails are...','Oregon trails','Travel','img2.jpg',1,800,'2024-01-20','2024-01-22');
INSERT INTO posts VALUES (3,'carol@blog.com','Best Tacos in Chicago','chicago-tacos','If you love tacos...','Taco tour','Food','img3.jpg',1,950,'2024-02-05','2024-02-05');
INSERT INTO posts VALUES (4,'alice@blog.com','React vs Vue in 2024','react-vue','Comparing frameworks...','Framework comparison','Web Dev','img4.jpg',1,2100,'2024-02-15','2024-02-20');
INSERT INTO posts VALUES (5,'eve@blog.com','Introduction to LLMs','intro-llms','Large language models...','LLM basics','AI/ML','img5.jpg',1,3200,'2024-03-01','2024-03-05');
INSERT INTO posts VALUES (6,'bob@blog.com','Budget Travel Tips','budget-travel','Save money while...','Budget tips','Travel','img6.jpg',1,600,'2024-03-10','2024-03-10');
INSERT INTO posts VALUES (7,'carol@blog.com','Homemade Pasta Guide','pasta-guide','Making pasta from...','Pasta tutorial','Food','img7.jpg',0,0,'2024-03-15',NULL);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    post_id INTEGER,
    commenter_email TEXT,
    commenter_name TEXT,
    body TEXT,
    is_approved INTEGER,
    parent_comment_id INTEGER,
    ip_address TEXT,
    likes_count INTEGER,
    created_at TEXT
);
INSERT INTO comments VALUES (1,1,'bob@blog.com','Bob Smith','Great tutorial!',1,NULL,'10.0.0.1',5,'2024-01-11');
INSERT INTO comments VALUES (2,1,'carol@blog.com','Carol Lee','Very helpful',1,NULL,'10.0.0.2',3,'2024-01-12');
INSERT INTO comments VALUES (3,1,'bob@blog.com','Bob Smith','Thanks for the update',1,1,'10.0.0.1',1,'2024-01-13');
INSERT INTO comments VALUES (4,3,'alice@blog.com','Alice Johnson','I agree!',1,NULL,'10.0.0.3',2,'2024-02-06');
INSERT INTO comments VALUES (5,5,'dave@blog.com','Dave Brown','Fascinating read',1,NULL,'10.0.0.4',8,'2024-03-02');
INSERT INTO comments VALUES (6,5,'frank@blog.com','Frank Wilson','Need more examples',0,NULL,'10.0.0.5',0,'2024-03-03');
INSERT INTO comments VALUES (7,4,'eve@blog.com','Eve Martinez','Vue is better IMO',1,NULL,'10.0.0.6',4,'2024-02-16');
INSERT INTO comments VALUES (8,2,'carol@blog.com','Carol Lee','Beautiful photos!',1,NULL,'10.0.0.2',2,'2024-01-21');

CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    name TEXT,
    slug TEXT,
    description TEXT,
    usage_count INTEGER,
    is_trending INTEGER,
    color TEXT,
    created_by_email TEXT,
    icon TEXT,
    created_at TEXT
);
INSERT INTO tags VALUES (1,'python','python','Python programming',3,1,'#3776AB','alice@blog.com','py-icon','2024-01-01');
INSERT INTO tags VALUES (2,'travel','travel','Travel content',2,0,'#2ECC71','bob@blog.com','travel-icon','2024-01-01');
INSERT INTO tags VALUES (3,'food','food','Food content',2,0,'#E74C3C','carol@blog.com','food-icon','2024-01-01');
INSERT INTO tags VALUES (4,'javascript','javascript','JS programming',2,1,'#F7DF1E','alice@blog.com','js-icon','2024-01-05');
INSERT INTO tags VALUES (5,'ai','ai','Artificial intelligence',1,1,'#9B59B6','eve@blog.com','ai-icon','2024-02-01');
INSERT INTO tags VALUES (6,'tutorial','tutorial','How-to guides',4,0,'#1ABC9C','alice@blog.com','tut-icon','2024-01-01');

CREATE TABLE post_tags (
    id INTEGER PRIMARY KEY,
    post_id INTEGER,
    tag_name TEXT,
    added_by_email TEXT,
    added_at TEXT,
    is_primary INTEGER,
    weight REAL,
    source TEXT,
    auto_tagged INTEGER,
    relevance_score REAL
);
INSERT INTO post_tags VALUES (1,1,'python','alice@blog.com','2024-01-10',1,1.0,'manual',0,0.95);
INSERT INTO post_tags VALUES (2,1,'tutorial','alice@blog.com','2024-01-10',0,0.8,'manual',0,0.85);
INSERT INTO post_tags VALUES (3,2,'travel','bob@blog.com','2024-01-20',1,1.0,'manual',0,0.90);
INSERT INTO post_tags VALUES (4,3,'food','carol@blog.com','2024-02-05',1,1.0,'manual',0,0.95);
INSERT INTO post_tags VALUES (5,4,'javascript','alice@blog.com','2024-02-15',1,1.0,'manual',0,0.90);
INSERT INTO post_tags VALUES (6,4,'tutorial','alice@blog.com','2024-02-15',0,0.7,'auto',1,0.75);
INSERT INTO post_tags VALUES (7,5,'ai','eve@blog.com','2024-03-01',1,1.0,'manual',0,0.98);
INSERT INTO post_tags VALUES (8,5,'python','eve@blog.com','2024-03-01',0,0.6,'auto',1,0.70);
INSERT INTO post_tags VALUES (9,5,'tutorial','eve@blog.com','2024-03-01',0,0.5,'auto',1,0.65);
INSERT INTO post_tags VALUES (10,6,'travel','bob@blog.com','2024-03-10',1,1.0,'manual',0,0.88);
INSERT INTO post_tags VALUES (11,3,'tutorial','carol@blog.com','2024-02-05',0,0.6,'auto',1,0.60);

CREATE TABLE likes (
    id INTEGER PRIMARY KEY,
    post_id INTEGER,
    user_email TEXT,
    reaction_type TEXT,
    liked_at TEXT,
    ip_address TEXT,
    user_agent TEXT,
    is_counted INTEGER,
    source_page TEXT,
    session_id TEXT
);
INSERT INTO likes VALUES (1,1,'bob@blog.com','like','2024-01-11','10.0.0.1','Mozilla/5.0',1,'/post/1','s001');
INSERT INTO likes VALUES (2,1,'carol@blog.com','love','2024-01-12','10.0.0.2','Chrome/120',1,'/post/1','s002');
INSERT INTO likes VALUES (3,5,'alice@blog.com','like','2024-03-02','10.0.0.3','Safari/17',1,'/post/5','s003');
INSERT INTO likes VALUES (4,5,'bob@blog.com','love','2024-03-02','10.0.0.1','Mozilla/5.0',1,'/post/5','s004');
INSERT INTO likes VALUES (5,4,'eve@blog.com','like','2024-02-16','10.0.0.6','Chrome/120',1,'/post/4','s005');
INSERT INTO likes VALUES (6,3,'dave@blog.com','like','2024-02-06','10.0.0.4','Safari/17',1,'/post/3','s006');
INSERT INTO likes VALUES (7,5,'dave@blog.com','like','2024-03-03','10.0.0.4','Safari/17',1,'/feed','s007');

CREATE TABLE followers (
    id INTEGER PRIMARY KEY,
    follower_email TEXT,
    following_email TEXT,
    followed_at TEXT,
    is_mutual INTEGER,
    notifications_on INTEGER,
    source TEXT,
    is_blocked INTEGER,
    is_muted INTEGER,
    notes TEXT
);
INSERT INTO followers VALUES (1,'bob@blog.com','alice@blog.com','2024-01-15',1,1,'profile',0,0,NULL);
INSERT INTO followers VALUES (2,'alice@blog.com','bob@blog.com','2024-01-16',1,1,'suggestion',0,0,NULL);
INSERT INTO followers VALUES (3,'carol@blog.com','alice@blog.com','2024-02-01',0,1,'profile',0,0,NULL);
INSERT INTO followers VALUES (4,'dave@blog.com','eve@blog.com','2024-03-01',0,1,'post',0,0,NULL);
INSERT INTO followers VALUES (5,'eve@blog.com','alice@blog.com','2024-03-02',0,0,'search',0,0,NULL);
INSERT INTO followers VALUES (6,'frank@blog.com','bob@blog.com','2024-03-15',0,1,'profile',0,0,NULL);

CREATE TABLE media (
    id INTEGER PRIMARY KEY,
    filename TEXT,
    url TEXT,
    mime_type TEXT,
    size_bytes INTEGER,
    width INTEGER,
    height INTEGER,
    uploader_email TEXT,
    post_id INTEGER,
    alt_text TEXT,
    created_at TEXT
);
INSERT INTO media VALUES (1,'img1.jpg','https://cdn.blog.com/img1.jpg','image/jpeg',245000,1920,1080,'alice@blog.com',1,'Python code screenshot','2024-01-10');
INSERT INTO media VALUES (2,'img2.jpg','https://cdn.blog.com/img2.jpg','image/jpeg',380000,2400,1600,'bob@blog.com',2,'Oregon trail photo','2024-01-20');
INSERT INTO media VALUES (3,'img3.jpg','https://cdn.blog.com/img3.jpg','image/jpeg',195000,1600,1200,'carol@blog.com',3,'Chicago tacos','2024-02-05');
INSERT INTO media VALUES (4,'img4.jpg','https://cdn.blog.com/img4.jpg','image/png',120000,1200,800,'alice@blog.com',4,'Framework comparison chart','2024-02-15');
INSERT INTO media VALUES (5,'img5.jpg','https://cdn.blog.com/img5.jpg','image/jpeg',290000,1920,1080,'eve@blog.com',5,'Neural network diagram','2024-03-01');
INSERT INTO media VALUES (6,'avatar-frank.jpg','https://cdn.blog.com/avatars/frank.jpg','image/jpeg',45000,400,400,'frank@blog.com',NULL,'Frank profile photo','2024-03-15');

CREATE TABLE settings (
    id INTEGER PRIMARY KEY,
    user_email TEXT,
    theme TEXT,
    language TEXT,
    timezone TEXT,
    email_notifications INTEGER,
    push_notifications INTEGER,
    privacy_level TEXT,
    two_factor_enabled INTEGER,
    last_login TEXT,
    login_count INTEGER
);
INSERT INTO settings VALUES (1,'alice@blog.com','dark','en','America/Chicago',1,1,'public',1,'2024-03-20',145);
INSERT INTO settings VALUES (2,'bob@blog.com','light','en','America/Los_Angeles',1,0,'public',0,'2024-03-18',89);
INSERT INTO settings VALUES (3,'carol@blog.com','dark','en','America/Chicago',1,1,'friends',0,'2024-03-19',112);
INSERT INTO settings VALUES (4,'dave@blog.com','light','en','America/New_York',0,0,'public',0,'2024-03-15',34);
INSERT INTO settings VALUES (5,'eve@blog.com','dark','en','America/Denver',1,1,'private',1,'2024-03-20',167);
INSERT INTO settings VALUES (6,'frank@blog.com','light','en','America/Los_Angeles',1,0,'public',0,'2024-03-16',12);
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
INSERT INTO users VALUES (1,'alice','alice@blog.com','h1','Alice Johnson','2024-01-01');
INSERT INTO users VALUES (2,'bob','bob@blog.com','h2','Bob Smith','2024-01-15');
INSERT INTO users VALUES (3,'carol','carol@blog.com','h3','Carol Lee','2024-02-01');
INSERT INTO users VALUES (4,'dave','dave@blog.com','h4','Dave Brown','2024-02-10');
INSERT INTO users VALUES (5,'eve','eve@blog.com','h5','Eve Martinez','2024-03-01');
INSERT INTO users VALUES (6,'frank','frank@blog.com','h6','Frank Wilson','2024-03-15');

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
