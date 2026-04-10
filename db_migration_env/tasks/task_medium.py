TASK_ID = "medium_instagram_migration"
DIFFICULTY = "medium"
TIMEOUT_SECONDS = 86400
MAX_STEPS = 12

TASK_DESCRIPTION = """
Facebook → Instagram-style Unified Schema Migration
======================================================

Facebook's legacy database (5 tables, fb_ prefix, email/username/group-name refs, zero FKs)
must be migrated into 8 Instagram-style tables. The polymorphic fb_likes table (post AND comment
likes in one table) must be split into post_likes and comment_likes. A computed account_stats
table must be derived. All 5 legacy tables must be dropped.

────────────────────────────────────────────────────────────────
 Table 1 / 8 : accounts
────────────────────────────────────────────────────────────────
4 rows from fb_users. id INTEGER PRIMARY KEY from uid, username TEXT NOT NULL UNIQUE from u_username, email TEXT NOT NULL UNIQUE from u_email, display_name TEXT NOT NULL computed as u_fname || ' ' || u_lname, created_at TEXT NOT NULL from u_joined, is_active INTEGER NOT NULL DEFAULT 1 from u_active.

────────────────────────────────────────────────────────────────
 Table 2 / 8 : media_posts
────────────────────────────────────────────────────────────────
4 rows from fb_posts. id INTEGER PRIMARY KEY from postid, author_id INTEGER NOT NULL FK→accounts(id) resolved by joining post_author_email against accounts.email, caption TEXT (nullable) from post_text, media_type TEXT NOT NULL DEFAULT 'photo' from post_type, created_at TEXT NOT NULL from post_created. Create index idx_posts_author on author_id.

────────────────────────────────────────────────────────────────
 Table 3 / 8 : post_comments
────────────────────────────────────────────────────────────────
4 rows from fb_comments. id INTEGER PRIMARY KEY from cmtid, post_id INTEGER NOT NULL FK→media_posts(id) from cmt_post_id, author_id INTEGER NOT NULL FK→accounts(id) resolved by joining cmt_author_email against accounts.email, parent_comment_id INTEGER FK→post_comments(id) (self-referential — from cmt_parent_id, NULL if top-level), content TEXT NOT NULL from cmt_text, created_at TEXT NOT NULL from cmt_created. Create index idx_comments_post on post_id.

────────────────────────────────────────────────────────────────
 Table 4 / 8 : post_likes
────────────────────────────────────────────────────────────────
3 rows from fb_likes WHERE like_target_type = 'post'. id INTEGER PRIMARY KEY (renumbered 1-3), post_id INTEGER NOT NULL FK→media_posts(id) from like_target_id, account_id INTEGER NOT NULL FK→accounts(id) resolved by joining like_user_email against accounts.email, created_at TEXT NOT NULL from like_created.

────────────────────────────────────────────────────────────────
 Table 5 / 8 : comment_likes
────────────────────────────────────────────────────────────────
2 rows from fb_likes WHERE like_target_type = 'comment'. id INTEGER PRIMARY KEY (renumbered 1-2), comment_id INTEGER NOT NULL FK→post_comments(id) from like_target_id, account_id INTEGER NOT NULL FK→accounts(id) resolved by joining like_user_email against accounts.email, created_at TEXT NOT NULL from like_created.

────────────────────────────────────────────────────────────────
 Table 6 / 8 : communities
────────────────────────────────────────────────────────────────
2 rows from fb_groups. id INTEGER PRIMARY KEY from gid, name TEXT NOT NULL UNIQUE from grp_name, description TEXT (nullable) from grp_desc, owner_id INTEGER NOT NULL FK→accounts(id) resolved by joining grp_owner_email against accounts.email, created_at TEXT NOT NULL from grp_created.

────────────────────────────────────────────────────────────────
 Table 7 / 8 : community_members
────────────────────────────────────────────────────────────────
3 rows from fb_group_members. id INTEGER PRIMARY KEY from gmid, community_id INTEGER NOT NULL FK→communities(id) resolved by joining gm_group_name against communities.name, account_id INTEGER NOT NULL FK→accounts(id) resolved by joining gm_user_email against accounts.email, role TEXT NOT NULL DEFAULT 'member' from gm_role, joined_at TEXT NOT NULL from gm_joined.

────────────────────────────────────────────────────────────────
 Table 8 / 8 : account_stats
────────────────────────────────────────────────────────────────
4 rows — one per account. id INTEGER PRIMARY KEY, account_id INTEGER NOT NULL UNIQUE FK→accounts(id), total_posts INTEGER NOT NULL DEFAULT 0 computed as COUNT of media_posts for this account, total_likes_received INTEGER NOT NULL DEFAULT 0 computed as COUNT of post_likes on posts authored by this account.

────────────────────────────────────────────────────────────────
 DROP ALL LEGACY TABLES: fb_users, fb_posts, fb_comments, fb_likes, fb_groups, fb_group_members.
"""

INITIAL_SQL = """
CREATE TABLE fb_users (
    uid INTEGER PRIMARY KEY,
    u_email TEXT NOT NULL,
    u_username TEXT NOT NULL,
    u_fname TEXT NOT NULL,
    u_lname TEXT NOT NULL,
    u_joined TEXT,
    u_active INTEGER DEFAULT 1
);

INSERT INTO fb_users VALUES (1, 'alice@email.com', 'alice_c', 'Alice', 'Chen', '2021-01-10', 1);
INSERT INTO fb_users VALUES (2, 'bob@email.com', 'bob_r', 'Bob', 'Rivera', '2021-03-05', 1);
INSERT INTO fb_users VALUES (3, 'carol@email.com', 'carol_z', 'Carol', 'Zhang', '2021-06-18', 1);
INSERT INTO fb_users VALUES (4, 'dave@email.com', 'dave_w', 'Dave', 'Wilson', '2022-01-12', 1);

CREATE TABLE fb_posts (
    postid INTEGER PRIMARY KEY,
    post_author_email TEXT NOT NULL,
    post_text TEXT,
    post_type TEXT DEFAULT 'photo',
    post_created TEXT
);

INSERT INTO fb_posts VALUES (1, 'alice@email.com', 'Beautiful sunset!', 'photo', '2024-01-15');
INSERT INTO fb_posts VALUES (2, 'bob@email.com', 'Check this recipe', 'text', '2024-01-20');
INSERT INTO fb_posts VALUES (3, 'carol@email.com', 'My new painting', 'photo', '2024-02-05');
INSERT INTO fb_posts VALUES (4, 'dave@email.com', 'Tech news roundup', 'link', '2024-03-01');

CREATE TABLE fb_comments (
    cmtid INTEGER PRIMARY KEY,
    cmt_post_id INTEGER NOT NULL,
    cmt_author_email TEXT NOT NULL,
    cmt_text TEXT NOT NULL,
    cmt_parent_id INTEGER,
    cmt_created TEXT
);

INSERT INTO fb_comments VALUES (1, 1, 'bob@email.com', 'Amazing photo!', NULL, '2024-01-15');
INSERT INTO fb_comments VALUES (2, 1, 'carol@email.com', 'Where was this?', NULL, '2024-01-16');
INSERT INTO fb_comments VALUES (3, 1, 'alice@email.com', 'At the coast!', 2, '2024-01-16');
INSERT INTO fb_comments VALUES (4, 3, 'dave@email.com', 'Love the colors!', NULL, '2024-02-06');

CREATE TABLE fb_likes (
    likeid INTEGER PRIMARY KEY,
    like_user_email TEXT NOT NULL,
    like_target_type TEXT NOT NULL,
    like_target_id INTEGER NOT NULL,
    like_created TEXT
);

INSERT INTO fb_likes VALUES (1, 'bob@email.com', 'post', 1, '2024-01-15');
INSERT INTO fb_likes VALUES (2, 'carol@email.com', 'post', 1, '2024-01-15');
INSERT INTO fb_likes VALUES (3, 'dave@email.com', 'post', 3, '2024-02-06');
INSERT INTO fb_likes VALUES (4, 'alice@email.com', 'comment', 1, '2024-01-16');
INSERT INTO fb_likes VALUES (5, 'carol@email.com', 'comment', 4, '2024-02-07');

CREATE TABLE fb_groups (
    gid INTEGER PRIMARY KEY,
    grp_name TEXT NOT NULL,
    grp_desc TEXT,
    grp_owner_email TEXT NOT NULL,
    grp_created TEXT
);

INSERT INTO fb_groups VALUES (1, 'Photography Club', 'Share your best shots', 'alice@email.com', '2023-06-01');
INSERT INTO fb_groups VALUES (2, 'Tech Enthusiasts', 'Discuss latest tech', 'dave@email.com', '2023-09-15');

CREATE TABLE fb_group_members (
    gmid INTEGER PRIMARY KEY,
    gm_group_name TEXT NOT NULL,
    gm_user_email TEXT NOT NULL,
    gm_role TEXT DEFAULT 'member',
    gm_joined TEXT
);

INSERT INTO fb_group_members VALUES (1, 'Photography Club', 'alice@email.com', 'admin', '2023-06-01');
INSERT INTO fb_group_members VALUES (2, 'Photography Club', 'bob@email.com', 'member', '2023-07-10');
INSERT INTO fb_group_members VALUES (3, 'Tech Enthusiasts', 'dave@email.com', 'admin', '2023-09-15');
"""

TARGET_SQL = """
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    created_at TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
);

INSERT INTO accounts VALUES (1, 'alice_c', 'alice@email.com', 'Alice Chen', '2021-01-10', 1);
INSERT INTO accounts VALUES (2, 'bob_r', 'bob@email.com', 'Bob Rivera', '2021-03-05', 1);
INSERT INTO accounts VALUES (3, 'carol_z', 'carol@email.com', 'Carol Zhang', '2021-06-18', 1);
INSERT INTO accounts VALUES (4, 'dave_w', 'dave@email.com', 'Dave Wilson', '2022-01-12', 1);

CREATE TABLE media_posts (
    id INTEGER PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES accounts(id),
    caption TEXT,
    media_type TEXT NOT NULL DEFAULT 'photo',
    created_at TEXT NOT NULL
);
CREATE INDEX idx_posts_author ON media_posts(author_id);

INSERT INTO media_posts VALUES (1, 1, 'Beautiful sunset!', 'photo', '2024-01-15');
INSERT INTO media_posts VALUES (2, 2, 'Check this recipe', 'text', '2024-01-20');
INSERT INTO media_posts VALUES (3, 3, 'My new painting', 'photo', '2024-02-05');
INSERT INTO media_posts VALUES (4, 4, 'Tech news roundup', 'link', '2024-03-01');

CREATE TABLE post_comments (
    id INTEGER PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES media_posts(id),
    author_id INTEGER NOT NULL REFERENCES accounts(id),
    parent_comment_id INTEGER REFERENCES post_comments(id),
    content TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE INDEX idx_comments_post ON post_comments(post_id);

INSERT INTO post_comments VALUES (1, 1, 2, NULL, 'Amazing photo!', '2024-01-15');
INSERT INTO post_comments VALUES (2, 1, 3, NULL, 'Where was this?', '2024-01-16');
INSERT INTO post_comments VALUES (3, 1, 1, 2, 'At the coast!', '2024-01-16');
INSERT INTO post_comments VALUES (4, 3, 4, NULL, 'Love the colors!', '2024-02-06');

CREATE TABLE post_likes (
    id INTEGER PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES media_posts(id),
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    created_at TEXT NOT NULL
);

INSERT INTO post_likes VALUES (1, 1, 2, '2024-01-15');
INSERT INTO post_likes VALUES (2, 1, 3, '2024-01-15');
INSERT INTO post_likes VALUES (3, 3, 4, '2024-02-06');

CREATE TABLE comment_likes (
    id INTEGER PRIMARY KEY,
    comment_id INTEGER NOT NULL REFERENCES post_comments(id),
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    created_at TEXT NOT NULL
);

INSERT INTO comment_likes VALUES (1, 1, 1, '2024-01-16');
INSERT INTO comment_likes VALUES (2, 4, 3, '2024-02-07');

CREATE TABLE communities (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    owner_id INTEGER NOT NULL REFERENCES accounts(id),
    created_at TEXT NOT NULL
);

INSERT INTO communities VALUES (1, 'Photography Club', 'Share your best shots', 1, '2023-06-01');
INSERT INTO communities VALUES (2, 'Tech Enthusiasts', 'Discuss latest tech', 4, '2023-09-15');

CREATE TABLE community_members (
    id INTEGER PRIMARY KEY,
    community_id INTEGER NOT NULL REFERENCES communities(id),
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    role TEXT NOT NULL DEFAULT 'member',
    joined_at TEXT NOT NULL
);

INSERT INTO community_members VALUES (1, 1, 1, 'admin', '2023-06-01');
INSERT INTO community_members VALUES (2, 1, 2, 'member', '2023-07-10');
INSERT INTO community_members VALUES (3, 2, 4, 'admin', '2023-09-15');

CREATE TABLE account_stats (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL UNIQUE REFERENCES accounts(id),
    total_posts INTEGER NOT NULL DEFAULT 0,
    total_likes_received INTEGER NOT NULL DEFAULT 0
);

INSERT INTO account_stats VALUES (1, 1, 1, 2);
INSERT INTO account_stats VALUES (2, 2, 1, 0);
INSERT INTO account_stats VALUES (3, 3, 1, 1);
INSERT INTO account_stats VALUES (4, 4, 1, 0);
"""
