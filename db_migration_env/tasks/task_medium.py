TASK_ID = "medium_instagram_migration"
DIFFICULTY = "medium"
TIMEOUT_SECONDS = 360  # 6 minutes

TASK_DESCRIPTION = """
Facebook → Instagram-style Unified Schema Migration
=====================================================

Meta is consolidating its social platforms. Facebook's entire 25-table legacy
database (all prefixed with fb_) must be migrated into a new 44-table Instagram-
style unified schema. Every table must be renamed, every email/username text
reference converted to integer foreign keys, and all data preserved with full
referential integrity. After migration, all 25 legacy fb_ tables must be dropped.

Below is the detailed specification for each target table.

────────────────────────────────────────────────────────────────
 Table  1 / 44 : accounts
────────────────────────────────────────────────────────────────
The accounts table serves as the foundation of the new identity layer, replacing Facebook's fb_users table with a properly normalized structure containing 10 rows. Each row is uniquely identified by an id INTEGER PRIMARY KEY, carried over directly from fb_users.uid. The username TEXT NOT NULL UNIQUE maps from u_username, email TEXT NOT NULL UNIQUE maps from u_email, phone TEXT maps from u_phone. Authentication data migrates from u_pass into password_hash TEXT NOT NULL. The account_status TEXT NOT NULL DEFAULT 'active' is set based on u_active (1 maps to 'active', 0 to 'inactive'). The account_type TEXT NOT NULL DEFAULT 'personal' is set to 'personal' for all migrated users. The created_at TEXT NOT NULL comes from u_joined, last_login_at TEXT is NULL for all migrated users, and is_verified INTEGER NOT NULL DEFAULT 0 is set to 0 for all users.

────────────────────────────────────────────────────────────────
 Table  2 / 44 : profiles
────────────────────────────────────────────────────────────────
The profiles table migrates 10 rows from fb_profiles. Each row has id INTEGER PRIMARY KEY from pid, and account_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining p_user_email against accounts.email. Columns: display_name TEXT is constructed from fb_users first and last name (u_fname || ' ' || u_lname), bio TEXT from p_bio, avatar_url TEXT from p_avatar, website TEXT from p_website, occupation TEXT from p_occupation, gender TEXT from p_gender, date_of_birth TEXT from fb_users.u_dob, city TEXT from fb_users.u_city, country TEXT from fb_users.u_country, is_public INTEGER NOT NULL DEFAULT 1 mapped from p_visibility where 'public' becomes 1 and 'private' becomes 0.

────────────────────────────────────────────────────────────────
 Table  3 / 44 : account_settings
────────────────────────────────────────────────────────────────
The account_settings table is derived from fb_privacy_settings with 10 rows. Each row has id INTEGER PRIMARY KEY from psid, account_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining ps_user_email against accounts.email. Columns: default_privacy TEXT NOT NULL DEFAULT 'public' from ps_post_default, notification_email INTEGER NOT NULL DEFAULT 1, notification_push INTEGER NOT NULL DEFAULT 1, notification_sms INTEGER NOT NULL DEFAULT 0, language TEXT NOT NULL DEFAULT 'en', theme TEXT NOT NULL DEFAULT 'light', two_factor_enabled INTEGER NOT NULL DEFAULT 0.

────────────────────────────────────────────────────────────────
 Table  4 / 44 : follow_relationships
────────────────────────────────────────────────────────────────
The follow_relationships table migrates 15 rows from fb_friendships. Since Facebook friendships are bidirectional but Instagram follows are directional, each fb_friendships row maps to one follow_relationships row with the first user following the second. Each row has id INTEGER PRIMARY KEY from fid, follower_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining f_user1_email against accounts.email, following_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining f_user2_email against accounts.email, status TEXT NOT NULL DEFAULT 'active' from f_status where 'accepted' maps to 'active' and 'pending' stays as 'pending', created_at TEXT NOT NULL from f_since.

────────────────────────────────────────────────────────────────
 Table  5 / 44 : blocked_accounts
────────────────────────────────────────────────────────────────
The blocked_accounts table migrates 5 rows from fb_blocked_users. Each row has id INTEGER PRIMARY KEY from blkid, blocker_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining blk_blocker_email against accounts.email, blocked_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining blk_blocked_email against accounts.email, reason TEXT from blk_reason, created_at TEXT NOT NULL from blk_created.

────────────────────────────────────────────────────────────────
 Table  6 / 44 : account_verifications
────────────────────────────────────────────────────────────────
The account_verifications table is entirely new and must be populated with 10 rows, one per account. Each row has id INTEGER PRIMARY KEY, account_id INTEGER NOT NULL REFERENCES accounts(id), verification_type TEXT NOT NULL DEFAULT 'email', verified_at TEXT set to the account's created_at date, document_url TEXT left as NULL.

────────────────────────────────────────────────────────────────
 Table  7 / 44 : media_posts
────────────────────────────────────────────────────────────────
The media_posts table migrates 20 rows from fb_posts. Each row has id INTEGER PRIMARY KEY from postid, author_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining post_author_email against accounts.email, caption TEXT from post_text, media_type TEXT NOT NULL DEFAULT 'photo' from post_type, media_url TEXT from post_media_url, thumbnail_url TEXT left as NULL, privacy TEXT NOT NULL DEFAULT 'public' from post_privacy, location TEXT left as NULL, is_archived INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL from post_created, updated_at TEXT from post_updated.

────────────────────────────────────────────────────────────────
 Table  8 / 44 : post_comments
────────────────────────────────────────────────────────────────
The post_comments table migrates 25 rows from fb_comments. Each row has id INTEGER PRIMARY KEY from cmtid, post_id INTEGER NOT NULL REFERENCES media_posts(id) from cmt_post_id, author_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining cmt_author_email against accounts.email, parent_comment_id INTEGER REFERENCES post_comments(id) from cmt_parent_id (NULL for top-level comments, self-referencing FK for replies), comment_text TEXT NOT NULL from cmt_text, is_edited INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL from cmt_created.

────────────────────────────────────────────────────────────────
 Table  9 / 44 : post_likes
────────────────────────────────────────────────────────────────
The post_likes table is derived from fb_likes where like_target_type is 'post', containing 18 rows. Each row has id INTEGER PRIMARY KEY (sequentially assigned), post_id INTEGER NOT NULL REFERENCES media_posts(id) from like_target_id, account_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining like_user_email against accounts.email, created_at TEXT NOT NULL from like_created.

────────────────────────────────────────────────────────────────
 Table 10 / 44 : comment_likes
────────────────────────────────────────────────────────────────
The comment_likes table is derived from fb_likes where like_target_type is 'comment', containing 12 rows. Each row has id INTEGER PRIMARY KEY (sequentially assigned), comment_id INTEGER NOT NULL REFERENCES post_comments(id) from like_target_id, account_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining like_user_email against accounts.email, created_at TEXT NOT NULL from like_created.

────────────────────────────────────────────────────────────────
 Table 11 / 44 : saved_posts
────────────────────────────────────────────────────────────────
The saved_posts table is derived from fb_saved_items where sav_target_type is 'post', containing 10 rows. Each row has id INTEGER PRIMARY KEY from savid, account_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining sav_user_email against accounts.email, post_id INTEGER NOT NULL REFERENCES media_posts(id) from sav_target_id, collection_name TEXT NOT NULL DEFAULT 'All Posts', saved_at TEXT NOT NULL from sav_created.

────────────────────────────────────────────────────────────────
 Table 12 / 44 : media_albums
────────────────────────────────────────────────────────────────
The media_albums table migrates 8 rows from fb_albums. Each row has id INTEGER PRIMARY KEY from albid, owner_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining alb_owner_email against accounts.email, album_name TEXT NOT NULL from alb_name, description TEXT from alb_desc, privacy TEXT NOT NULL DEFAULT 'public' from alb_privacy, cover_url TEXT from alb_cover_url, created_at TEXT NOT NULL from alb_created, updated_at TEXT left as NULL.

────────────────────────────────────────────────────────────────
 Table 13 / 44 : album_media
────────────────────────────────────────────────────────────────
The album_media table is a new junction table linking albums to posts, containing 8 rows. Each row has id INTEGER PRIMARY KEY, album_id INTEGER NOT NULL REFERENCES media_albums(id), post_id INTEGER NOT NULL REFERENCES media_posts(id), sort_order INTEGER NOT NULL DEFAULT 0, added_at TEXT NOT NULL. This is derived by matching fb_photos.ph_album_name to media_albums and linking photos to their corresponding media_posts by author.

────────────────────────────────────────────────────────────────
 Table 14 / 44 : hashtags
────────────────────────────────────────────────────────────────
The hashtags table migrates 8 rows from fb_hashtags. Each row has id INTEGER PRIMARY KEY from hashid, tag_name TEXT NOT NULL UNIQUE from hash_tag, usage_count INTEGER NOT NULL DEFAULT 0 from hash_post_count, is_trending INTEGER NOT NULL DEFAULT 0 set to 1 for tags with post_count >= 3, created_at TEXT NOT NULL from hash_created.

────────────────────────────────────────────────────────────────
 Table 15 / 44 : post_hashtags
────────────────────────────────────────────────────────────────
The post_hashtags table migrates 15 rows from fb_post_hashtags. Each row has id INTEGER PRIMARY KEY from phashid, post_id INTEGER NOT NULL REFERENCES media_posts(id) from phash_post_id, hashtag_id INTEGER NOT NULL REFERENCES hashtags(id) resolved by joining phash_tag_text against hashtags.tag_name, created_at TEXT NOT NULL from phash_created.

────────────────────────────────────────────────────────────────
 Table 16 / 44 : post_mentions
────────────────────────────────────────────────────────────────
The post_mentions table is new and derived from scanning post content for @username references, containing 6 rows. Each row has id INTEGER PRIMARY KEY, post_id INTEGER NOT NULL REFERENCES media_posts(id), mentioned_account_id INTEGER NOT NULL REFERENCES accounts(id), created_at TEXT NOT NULL matching the post's created_at.

────────────────────────────────────────────────────────────────
 Table 17 / 44 : post_shares
────────────────────────────────────────────────────────────────
The post_shares table is new, containing 5 rows representing shares derived from fb_posts share counts. Each row has id INTEGER PRIMARY KEY, original_post_id INTEGER NOT NULL REFERENCES media_posts(id), shared_by_id INTEGER NOT NULL REFERENCES accounts(id), share_type TEXT NOT NULL DEFAULT 'repost', shared_at TEXT NOT NULL.

────────────────────────────────────────────────────────────────
 Table 18 / 44 : stories
────────────────────────────────────────────────────────────────
The stories table is new, derived from fb_posts where post_type is 'photo', containing 5 rows representing stories. Each row has id INTEGER PRIMARY KEY, author_id INTEGER NOT NULL REFERENCES accounts(id), media_url TEXT NOT NULL, media_type TEXT NOT NULL DEFAULT 'photo', caption TEXT, created_at TEXT NOT NULL, expires_at TEXT NOT NULL (set to 24 hours after created_at), is_highlight INTEGER NOT NULL DEFAULT 0.

────────────────────────────────────────────────────────────────
 Table 19 / 44 : story_views
────────────────────────────────────────────────────────────────
The story_views table is new, containing 10 rows. Each row has id INTEGER PRIMARY KEY, story_id INTEGER NOT NULL REFERENCES stories(id), viewer_id INTEGER NOT NULL REFERENCES accounts(id), viewed_at TEXT NOT NULL.

────────────────────────────────────────────────────────────────
 Table 20 / 44 : story_highlights
────────────────────────────────────────────────────────────────
The story_highlights table is new, containing 4 rows. Each row has id INTEGER PRIMARY KEY, account_id INTEGER NOT NULL REFERENCES accounts(id), highlight_name TEXT NOT NULL, cover_url TEXT, created_at TEXT NOT NULL.

────────────────────────────────────────────────────────────────
 Table 21 / 44 : communities
────────────────────────────────────────────────────────────────
The communities table migrates 6 rows from fb_groups. Each row has id INTEGER PRIMARY KEY from gid, name TEXT NOT NULL from g_name, slug TEXT NOT NULL derived from g_name lowercased with spaces replaced by hyphens, description TEXT from g_desc, creator_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining g_creator_email against accounts.email, privacy TEXT NOT NULL DEFAULT 'public' from g_privacy, cover_url TEXT left as NULL, member_count INTEGER NOT NULL DEFAULT 0 from g_member_count, created_at TEXT NOT NULL from g_created, is_active INTEGER NOT NULL DEFAULT 1.

────────────────────────────────────────────────────────────────
 Table 22 / 44 : community_members
────────────────────────────────────────────────────────────────
The community_members table migrates 18 rows from fb_group_members. Each row has id INTEGER PRIMARY KEY from gmid, community_id INTEGER NOT NULL REFERENCES communities(id) resolved by joining gm_group_name against communities.name, account_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining gm_user_email against accounts.email, role TEXT NOT NULL DEFAULT 'member' from gm_role, joined_at TEXT NOT NULL from gm_joined, is_active INTEGER NOT NULL DEFAULT 1.

────────────────────────────────────────────────────────────────
 Table 23 / 44 : community_posts
────────────────────────────────────────────────────────────────
The community_posts table migrates 12 rows from fb_group_posts. Each row has id INTEGER PRIMARY KEY from gpid, community_id INTEGER NOT NULL REFERENCES communities(id) resolved by joining gp_group_name against communities.name, author_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining gp_author_email against accounts.email, content TEXT NOT NULL from gp_text, media_url TEXT from gp_media_url, created_at TEXT NOT NULL from gp_created.

────────────────────────────────────────────────────────────────
 Table 24 / 44 : community_rules
────────────────────────────────────────────────────────────────
The community_rules table is new, containing 6 rows with one rule per community. Each row has id INTEGER PRIMARY KEY, community_id INTEGER NOT NULL REFERENCES communities(id), rule_text TEXT NOT NULL, sort_order INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL.

────────────────────────────────────────────────────────────────
 Table 25 / 44 : creator_accounts
────────────────────────────────────────────────────────────────
The creator_accounts table migrates 5 rows from fb_pages. Each row has id INTEGER PRIMARY KEY from pageid, account_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining pg_owner_email against accounts.email, page_name TEXT NOT NULL from pg_name, category TEXT NOT NULL from pg_category, description TEXT from pg_desc, website TEXT from pg_website, contact_email TEXT from pg_owner_email, is_verified INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL from pg_created.

────────────────────────────────────────────────────────────────
 Table 26 / 44 : creator_followers
────────────────────────────────────────────────────────────────
The creator_followers table migrates 12 rows from fb_page_followers. Each row has id INTEGER PRIMARY KEY from pfid, creator_account_id INTEGER NOT NULL REFERENCES creator_accounts(id) resolved by joining pf_page_name against creator_accounts.page_name, follower_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining pf_user_email against accounts.email, followed_at TEXT NOT NULL from pf_followed_since.

────────────────────────────────────────────────────────────────
 Table 27 / 44 : creator_insights
────────────────────────────────────────────────────────────────
The creator_insights table is computed, containing 5 rows, one per creator account. Each row has id INTEGER PRIMARY KEY, creator_account_id INTEGER NOT NULL REFERENCES creator_accounts(id), total_followers INTEGER NOT NULL DEFAULT 0 computed by counting rows in creator_followers for that creator, total_posts INTEGER NOT NULL DEFAULT 0 computed by counting media_posts by the creator's linked account, avg_engagement_rate REAL computed as the average likes per post for the creator's content.

────────────────────────────────────────────────────────────────
 Table 28 / 44 : dm_threads
────────────────────────────────────────────────────────────────
The dm_threads table migrates 8 rows from fb_conversations. Each row has id INTEGER PRIMARY KEY from convid, created_at TEXT NOT NULL from conv_created, updated_at TEXT from conv_last_msg, is_group_chat INTEGER NOT NULL DEFAULT 0.

────────────────────────────────────────────────────────────────
 Table 29 / 44 : dm_participants
────────────────────────────────────────────────────────────────
The dm_participants table is derived from fb_conversations, containing 16 rows (two participants per conversation). Each row has id INTEGER PRIMARY KEY, thread_id INTEGER NOT NULL REFERENCES dm_threads(id), account_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining conv_user1_email or conv_user2_email against accounts.email, joined_at TEXT NOT NULL from conv_created, is_muted INTEGER NOT NULL DEFAULT 0.

────────────────────────────────────────────────────────────────
 Table 30 / 44 : dm_messages
────────────────────────────────────────────────────────────────
The dm_messages table migrates 20 rows from fb_messages. Each row has id INTEGER PRIMARY KEY from msgid, thread_id INTEGER NOT NULL REFERENCES dm_threads(id) from msg_conv_id, sender_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining msg_sender_email against accounts.email, message_text TEXT from msg_text, media_url TEXT from msg_media_url, sent_at TEXT NOT NULL from msg_sent, read_at TEXT from msg_read, is_deleted INTEGER NOT NULL DEFAULT 0.

────────────────────────────────────────────────────────────────
 Table 31 / 44 : events
────────────────────────────────────────────────────────────────
The events table migrates 6 rows from fb_events. Each row has id INTEGER PRIMARY KEY from evid, creator_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining ev_creator_email against accounts.email, event_name TEXT NOT NULL from ev_name, description TEXT from ev_desc, location TEXT from ev_location, start_time TEXT NOT NULL from ev_start, end_time TEXT from ev_end, privacy TEXT NOT NULL DEFAULT 'public' from ev_privacy, cover_url TEXT left as NULL, created_at TEXT NOT NULL from ev_created, is_cancelled INTEGER NOT NULL DEFAULT 0.

────────────────────────────────────────────────────────────────
 Table 32 / 44 : event_attendees
────────────────────────────────────────────────────────────────
The event_attendees table migrates 15 rows from fb_event_rsvps. Each row has id INTEGER PRIMARY KEY from rsvpid, event_id INTEGER NOT NULL REFERENCES events(id) resolved by joining rsvp_event_name against events.event_name, account_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining rsvp_user_email against accounts.email, rsvp_status TEXT NOT NULL DEFAULT 'invited' from rsvp_status, responded_at TEXT from rsvp_created.

────────────────────────────────────────────────────────────────
 Table 33 / 44 : event_posts
────────────────────────────────────────────────────────────────
The event_posts table is new, containing 6 rows — one per event. The event creator posts an announcement for their own event. Each row has id INTEGER PRIMARY KEY assigned sequentially matching the event_id, event_id INTEGER NOT NULL REFERENCES events(id), author_id INTEGER NOT NULL REFERENCES accounts(id) set to the creator_id of that event, content TEXT NOT NULL which is a short announcement message from the host, media_url TEXT which is NULL for most but may include an image path like '/media/events/name_desc.jpg' for events 2 and 5, created_at TEXT NOT NULL matching the event's start_time date.

────────────────────────────────────────────────────────────────
 Table 34 / 44 : content_reports
────────────────────────────────────────────────────────────────
The content_reports table migrates 6 rows from fb_reports. Each row has id INTEGER PRIMARY KEY from repid, reporter_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining rep_reporter_email against accounts.email, content_type TEXT NOT NULL from rep_target_type, content_id INTEGER NOT NULL from rep_target_id, reason TEXT NOT NULL from rep_reason, status TEXT NOT NULL DEFAULT 'pending' from rep_status, created_at TEXT NOT NULL from rep_created, reviewed_at TEXT left as NULL, reviewer_notes TEXT left as NULL.

────────────────────────────────────────────────────────────────
 Table 35 / 44 : moderation_actions
────────────────────────────────────────────────────────────────
The moderation_actions table is new, containing 6 rows, one per content report — every report gets an automatic moderation action. Each row has id INTEGER PRIMARY KEY matching the report id, report_id INTEGER NOT NULL REFERENCES content_reports(id) matching sequentially, action_type TEXT NOT NULL DEFAULT 'review' which is 'review' for all reports except report 5 where it is 'dismiss', action_by TEXT NOT NULL DEFAULT 'system' always set to 'system', notes TEXT describing the action taken (e.g. 'Content reviewed and flagged', 'Pending manual review', 'Content reviewed and removed', or 'Report dismissed after review' for dismissed ones), created_at TEXT NOT NULL set to one day after the content_report's created_at.

────────────────────────────────────────────────────────────────
 Table 36 / 44 : activity_log
────────────────────────────────────────────────────────────────
The activity_log table migrates 15 rows from fb_activity_log. Each row has id INTEGER PRIMARY KEY from actid, account_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining act_user_email against accounts.email, activity_type TEXT NOT NULL from act_type, description TEXT from act_detail, target_type TEXT from act_target_type, target_id INTEGER from act_target_id, ip_address TEXT left as NULL, created_at TEXT NOT NULL from act_created.

────────────────────────────────────────────────────────────────
 Table 37 / 44 : notification_preferences
────────────────────────────────────────────────────────────────
The notification_preferences table is new, derived from fb_privacy_settings, containing 10 rows. Each row has id INTEGER PRIMARY KEY, account_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining ps_user_email against accounts.email, likes_notify INTEGER NOT NULL DEFAULT 1, comments_notify INTEGER NOT NULL DEFAULT 1, follows_notify INTEGER NOT NULL DEFAULT 1, dm_notify INTEGER NOT NULL DEFAULT 1, mentions_notify INTEGER NOT NULL DEFAULT 1.

────────────────────────────────────────────────────────────────
 Table 38 / 44 : notifications
────────────────────────────────────────────────────────────────
The notifications table migrates 20 rows from fb_notifications. Each row has id INTEGER PRIMARY KEY from notifid, account_id INTEGER NOT NULL REFERENCES accounts(id) resolved by joining notif_user_email against accounts.email, notification_type TEXT NOT NULL from notif_type, title TEXT NOT NULL mapped from notif_type using these rules: 'like' becomes 'New Like', 'comment' becomes 'New Comment', 'friend_request' becomes 'Follow Request', 'event' becomes 'Event Invite', 'group' becomes 'Community Update', 'page' becomes 'Creator Update'. The body TEXT is taken directly from notif_text, is_read INTEGER NOT NULL DEFAULT 0 from notif_read, source_type TEXT is the same as notif_type, source_id INTEGER from notif_source_id (NULL for friend_request notifications), created_at TEXT NOT NULL from notif_created.

────────────────────────────────────────────────────────────────
 Table 39 / 44 : account_stats
────────────────────────────────────────────────────────────────
The account_stats table is a computed summary with 10 rows, one per account. Each row has id INTEGER PRIMARY KEY, account_id INTEGER NOT NULL REFERENCES accounts(id). The post_count INTEGER NOT NULL DEFAULT 0 is COUNT(*) FROM media_posts WHERE author_id equals the account id — returns 0 for accounts with no posts. The follower_count INTEGER NOT NULL DEFAULT 0 is COUNT(*) FROM follow_relationships WHERE following_id equals the account id — this counts how many people follow this account. The following_count INTEGER NOT NULL DEFAULT 0 is COUNT(*) FROM follow_relationships WHERE follower_id equals the account id — this counts how many people this account follows. The total_likes_received INTEGER NOT NULL DEFAULT 0 is COUNT(*) FROM post_likes WHERE post_id is in the set of media_posts authored by this account — join post_likes to media_posts on post_id to group by author_id.

────────────────────────────────────────────────────────────────
 Table 40 / 44 : post_analytics
────────────────────────────────────────────────────────────────
The post_analytics table is a computed summary with 20 rows, one per media post. Each row has id INTEGER PRIMARY KEY matching the post_id, post_id INTEGER NOT NULL REFERENCES media_posts(id). The like_count INTEGER NOT NULL DEFAULT 0 is COUNT(*) FROM post_likes WHERE post_likes.post_id matches this post. The comment_count INTEGER NOT NULL DEFAULT 0 is COUNT(*) FROM post_comments WHERE post_comments.post_id matches this post (only direct comments, not replies to comments). The share_count INTEGER NOT NULL DEFAULT 0 is COUNT(*) FROM post_shares WHERE post_shares.original_post_id matches this post. The save_count INTEGER NOT NULL DEFAULT 0 is COUNT(*) FROM saved_posts WHERE saved_posts.post_id matches this post. The view_count INTEGER NOT NULL DEFAULT 0 is estimated as (like_count + comment_count) multiplied by 10, with a minimum of 10 for posts that have any likes or comments, and 0 for posts with no engagement at all — use CASE WHEN (like_count + comment_count) > 0 THEN (like_count + comment_count) * 10 ELSE 0 END.

────────────────────────────────────────────────────────────────
 Table 41 / 44 : engagement_daily
────────────────────────────────────────────────────────────────
The engagement_daily table is a computed summary aggregated by month, containing 4 rows — one per distinct YYYY-MM month found in media_posts.created_at. Each row has id INTEGER PRIMARY KEY assigned sequentially by month order using ROW_NUMBER() OVER (ORDER BY month), summary_date TEXT NOT NULL which is the YYYY-MM string (e.g. '2024-01'), total_posts INTEGER NOT NULL DEFAULT 0 is COUNT(*) FROM media_posts WHERE SUBSTR(created_at,1,7) matches the month, total_likes INTEGER NOT NULL DEFAULT 0 is COUNT(*) FROM post_likes WHERE SUBSTR(created_at,1,7) matches the month, total_comments INTEGER NOT NULL DEFAULT 0 is COUNT(*) FROM post_comments WHERE SUBSTR(created_at,1,7) matches the month, total_new_accounts INTEGER NOT NULL DEFAULT 0 is COUNT(*) FROM accounts WHERE SUBSTR(created_at,1,7) matches the month — this will be 0 for all rows since all accounts were created before 2024.

────────────────────────────────────────────────────────────────
 Table 42 / 44 : hashtag_trends
────────────────────────────────────────────────────────────────
The hashtag_trends table is a computed summary with 8 rows, one per hashtag. Each row has id INTEGER PRIMARY KEY matching the hashtag id, hashtag_id INTEGER NOT NULL REFERENCES hashtags(id), period TEXT NOT NULL always set to '2024-Q1' for this migration, post_count INTEGER NOT NULL DEFAULT 0 is COUNT(*) FROM post_hashtags WHERE hashtag_id matches this hashtag, engagement_score REAL NOT NULL DEFAULT 0.0 is computed as post_count multiplied by 2.5 — use ROUND(post_count * 2.5, 1).

────────────────────────────────────────────────────────────────
 Table 43 / 44 : community_stats
────────────────────────────────────────────────────────────────
The community_stats table is a computed summary with 6 rows, one per community. Each row has id INTEGER PRIMARY KEY matching the community id, community_id INTEGER NOT NULL REFERENCES communities(id), total_posts INTEGER NOT NULL DEFAULT 0 is COUNT(*) FROM community_posts WHERE community_id matches, total_members INTEGER NOT NULL DEFAULT 0 is COUNT(*) FROM community_members WHERE community_id matches, active_members INTEGER NOT NULL DEFAULT 0 is COUNT(DISTINCT author_id) FROM community_posts WHERE community_id matches — this counts only members who have actually posted.

────────────────────────────────────────────────────────────────
 Table 44 / 44 : migration_log
────────────────────────────────────────────────────────────────
The migration_log table is new, containing 25 rows — one entry per legacy-to-target table mapping. Each row has id INTEGER PRIMARY KEY assigned sequentially, source_table TEXT NOT NULL which is the fb_ table name, target_table TEXT NOT NULL which is the corresponding target table name, rows_migrated INTEGER NOT NULL DEFAULT 0 set to the actual row count inserted into the target table, migrated_at TEXT NOT NULL set to sequential timestamps starting from '2024-04-15 10:00:00' with one minute increments. The 25 mappings in order are: fb_users→accounts (10), fb_profiles→profiles (10), fb_privacy_settings→account_settings (10), fb_friendships→follow_relationships (15), fb_blocked_users→blocked_accounts (5), fb_users→account_verifications (10), fb_posts→media_posts (20), fb_comments→post_comments (25), fb_likes→post_likes (18), fb_likes→comment_likes (12), fb_saved_items→saved_posts (10), fb_albums→media_albums (8), fb_photos→album_media (8), fb_hashtags→hashtags (8), fb_post_hashtags→post_hashtags (15), fb_posts→post_mentions (6), fb_posts→post_shares (5), fb_posts→stories (5), fb_groups→communities (6), fb_group_members→community_members (18), fb_group_posts→community_posts (12), fb_pages→creator_accounts (5), fb_page_followers→creator_followers (12), fb_conversations→dm_threads (8), fb_messages→dm_messages (20).

────────────────────────────────────────────────────────────────
 Legacy Cleanup
────────────────────────────────────────────────────────────────
Drop all 25 fb_ tables: fb_users, fb_profiles, fb_friendships, fb_posts, fb_comments, fb_likes, fb_photos, fb_albums, fb_groups, fb_group_members, fb_group_posts, fb_pages, fb_page_followers, fb_conversations, fb_messages, fb_events, fb_event_rsvps, fb_notifications, fb_activity_log, fb_reports, fb_privacy_settings, fb_blocked_users, fb_saved_items, fb_hashtags, fb_post_hashtags.

"""

INITIAL_SQL = """
-- Facebook Legacy Schema
-- No foreign keys, no indexes, text-based references everywhere

-- =============================================
-- fb_users (10 rows)
-- =============================================
CREATE TABLE fb_users (
    uid INTEGER PRIMARY KEY,
    u_email TEXT NOT NULL,
    u_username TEXT NOT NULL,
    u_fname TEXT NOT NULL,
    u_lname TEXT NOT NULL,
    u_pass TEXT NOT NULL,
    u_phone TEXT,
    u_dob TEXT,
    u_city TEXT,
    u_country TEXT,
    u_joined TEXT,
    u_active INTEGER DEFAULT 1
);

INSERT INTO fb_users (uid, u_email, u_username, u_fname, u_lname, u_pass, u_phone, u_dob, u_city, u_country, u_joined, u_active) VALUES (1, 'alice@facebook.com', 'alice_chen', 'Alice', 'Chen', 'hashed_pw_alice01', '555-0101', '1990-03-15', 'San Francisco', 'US', '2020-01-15', 1);
INSERT INTO fb_users (uid, u_email, u_username, u_fname, u_lname, u_pass, u_phone, u_dob, u_city, u_country, u_joined, u_active) VALUES (2, 'bob@facebook.com', 'bob_rivera', 'Bob', 'Rivera', 'hashed_pw_bob02', '555-0102', '1985-07-22', 'Austin', 'US', '2020-03-10', 1);
INSERT INTO fb_users (uid, u_email, u_username, u_fname, u_lname, u_pass, u_phone, u_dob, u_city, u_country, u_joined, u_active) VALUES (3, 'carol@facebook.com', 'carol_zhang', 'Carol', 'Zhang', 'hashed_pw_carol03', '555-0103', '1992-11-08', 'Seattle', 'US', '2020-06-20', 1);
INSERT INTO fb_users (uid, u_email, u_username, u_fname, u_lname, u_pass, u_phone, u_dob, u_city, u_country, u_joined, u_active) VALUES (4, 'dave@facebook.com', 'dave_wilson', 'Dave', 'Wilson', 'hashed_pw_dave04', '555-0104', '1988-01-30', 'Denver', 'US', '2020-09-05', 1);
INSERT INTO fb_users (uid, u_email, u_username, u_fname, u_lname, u_pass, u_phone, u_dob, u_city, u_country, u_joined, u_active) VALUES (5, 'eve@facebook.com', 'eve_thompson', 'Eve', 'Thompson', 'hashed_pw_eve05', '555-0105', '1995-05-12', 'Miami', 'US', '2021-01-10', 1);
INSERT INTO fb_users (uid, u_email, u_username, u_fname, u_lname, u_pass, u_phone, u_dob, u_city, u_country, u_joined, u_active) VALUES (6, 'frank@facebook.com', 'frank_garcia', 'Frank', 'Garcia', 'hashed_pw_frank06', '555-0106', '1983-09-25', 'Chicago', 'US', '2021-04-18', 1);
INSERT INTO fb_users (uid, u_email, u_username, u_fname, u_lname, u_pass, u_phone, u_dob, u_city, u_country, u_joined, u_active) VALUES (7, 'grace@facebook.com', 'grace_kim', 'Grace', 'Kim', 'hashed_pw_grace07', '555-0107', '1991-12-03', 'Los Angeles', 'US', '2021-07-22', 1);
INSERT INTO fb_users (uid, u_email, u_username, u_fname, u_lname, u_pass, u_phone, u_dob, u_city, u_country, u_joined, u_active) VALUES (8, 'henry@facebook.com', 'henry_patel', 'Henry', 'Patel', 'hashed_pw_henry08', '555-0108', '1987-04-18', 'Boston', 'US', '2021-10-30', 1);
INSERT INTO fb_users (uid, u_email, u_username, u_fname, u_lname, u_pass, u_phone, u_dob, u_city, u_country, u_joined, u_active) VALUES (9, 'ivy@facebook.com', 'ivy_santos', 'Ivy', 'Santos', 'hashed_pw_ivy09', '555-0109', '1994-08-07', 'Phoenix', 'US', '2022-02-14', 1);
INSERT INTO fb_users (uid, u_email, u_username, u_fname, u_lname, u_pass, u_phone, u_dob, u_city, u_country, u_joined, u_active) VALUES (10, 'jack@facebook.com', 'jack_murphy', 'Jack', 'Murphy', 'hashed_pw_jack10', '555-0110', '1986-02-14', 'Nashville', 'US', '2022-05-01', 1);

-- =============================================
-- fb_profiles (10 rows)
-- =============================================
CREATE TABLE fb_profiles (
    pid INTEGER PRIMARY KEY,
    p_user_email TEXT NOT NULL,
    p_bio TEXT,
    p_avatar TEXT,
    p_cover TEXT,
    p_website TEXT,
    p_occupation TEXT,
    p_gender TEXT,
    p_visibility TEXT DEFAULT 'public'
);

INSERT INTO fb_profiles (pid, p_user_email, p_bio, p_avatar, p_cover, p_website, p_occupation, p_gender, p_visibility) VALUES (1, 'alice@facebook.com', 'Tech enthusiast and photographer', '/avatars/alice.jpg', '/covers/alice.jpg', 'https://alicechen.dev', 'Software Engineer', 'female', 'public');
INSERT INTO fb_profiles (pid, p_user_email, p_bio, p_avatar, p_cover, p_website, p_occupation, p_gender, p_visibility) VALUES (2, 'bob@facebook.com', 'Music lover and foodie', '/avatars/bob.jpg', '/covers/bob.jpg', NULL, 'Chef', 'male', 'public');
INSERT INTO fb_profiles (pid, p_user_email, p_bio, p_avatar, p_cover, p_website, p_occupation, p_gender, p_visibility) VALUES (3, 'carol@facebook.com', 'Travel blogger exploring the world', '/avatars/carol.jpg', '/covers/carol.jpg', 'https://carolztravels.com', 'Travel Blogger', 'female', 'public');
INSERT INTO fb_profiles (pid, p_user_email, p_bio, p_avatar, p_cover, p_website, p_occupation, p_gender, p_visibility) VALUES (4, 'dave@facebook.com', 'Outdoor adventurer and fitness buff', '/avatars/dave.jpg', '/covers/dave.jpg', NULL, 'Personal Trainer', 'male', 'private');
INSERT INTO fb_profiles (pid, p_user_email, p_bio, p_avatar, p_cover, p_website, p_occupation, p_gender, p_visibility) VALUES (5, 'eve@facebook.com', 'Digital artist and designer', '/avatars/eve.jpg', '/covers/eve.jpg', 'https://evedesigns.co', 'Graphic Designer', 'female', 'public');
INSERT INTO fb_profiles (pid, p_user_email, p_bio, p_avatar, p_cover, p_website, p_occupation, p_gender, p_visibility) VALUES (6, 'frank@facebook.com', 'Startup founder and mentor', '/avatars/frank.jpg', '/covers/frank.jpg', 'https://frankgarcia.biz', 'Entrepreneur', 'male', 'public');
INSERT INTO fb_profiles (pid, p_user_email, p_bio, p_avatar, p_cover, p_website, p_occupation, p_gender, p_visibility) VALUES (7, 'grace@facebook.com', 'Film critic and cinephile', '/avatars/grace.jpg', '/covers/grace.jpg', NULL, 'Film Critic', 'female', 'public');
INSERT INTO fb_profiles (pid, p_user_email, p_bio, p_avatar, p_cover, p_website, p_occupation, p_gender, p_visibility) VALUES (8, 'henry@facebook.com', 'Data scientist by day, gamer by night', '/avatars/henry.jpg', '/covers/henry.jpg', 'https://henrypatel.io', 'Data Scientist', 'male', 'private');
INSERT INTO fb_profiles (pid, p_user_email, p_bio, p_avatar, p_cover, p_website, p_occupation, p_gender, p_visibility) VALUES (9, 'ivy@facebook.com', 'Yoga instructor and wellness coach', '/avatars/ivy.jpg', '/covers/ivy.jpg', 'https://ivywellness.com', 'Yoga Instructor', 'female', 'public');
INSERT INTO fb_profiles (pid, p_user_email, p_bio, p_avatar, p_cover, p_website, p_occupation, p_gender, p_visibility) VALUES (10, 'jack@facebook.com', 'Musician and songwriter', '/avatars/jack.jpg', '/covers/jack.jpg', 'https://jackmurphymusic.com', 'Musician', 'male', 'public');

-- =============================================
-- fb_friendships (15 rows)
-- =============================================
CREATE TABLE fb_friendships (
    fid INTEGER PRIMARY KEY,
    f_user1_email TEXT NOT NULL,
    f_user2_email TEXT NOT NULL,
    f_status TEXT DEFAULT 'accepted',
    f_since TEXT
);

INSERT INTO fb_friendships (fid, f_user1_email, f_user2_email, f_status, f_since) VALUES (1, 'alice@facebook.com', 'bob@facebook.com', 'accepted', '2020-04-01');
INSERT INTO fb_friendships (fid, f_user1_email, f_user2_email, f_status, f_since) VALUES (2, 'alice@facebook.com', 'carol@facebook.com', 'accepted', '2020-07-15');
INSERT INTO fb_friendships (fid, f_user1_email, f_user2_email, f_status, f_since) VALUES (3, 'alice@facebook.com', 'dave@facebook.com', 'accepted', '2020-10-20');
INSERT INTO fb_friendships (fid, f_user1_email, f_user2_email, f_status, f_since) VALUES (4, 'bob@facebook.com', 'carol@facebook.com', 'accepted', '2020-08-05');
INSERT INTO fb_friendships (fid, f_user1_email, f_user2_email, f_status, f_since) VALUES (5, 'bob@facebook.com', 'eve@facebook.com', 'accepted', '2021-02-14');
INSERT INTO fb_friendships (fid, f_user1_email, f_user2_email, f_status, f_since) VALUES (6, 'carol@facebook.com', 'frank@facebook.com', 'accepted', '2021-05-10');
INSERT INTO fb_friendships (fid, f_user1_email, f_user2_email, f_status, f_since) VALUES (7, 'dave@facebook.com', 'grace@facebook.com', 'accepted', '2021-08-22');
INSERT INTO fb_friendships (fid, f_user1_email, f_user2_email, f_status, f_since) VALUES (8, 'eve@facebook.com', 'henry@facebook.com', 'accepted', '2021-11-30');
INSERT INTO fb_friendships (fid, f_user1_email, f_user2_email, f_status, f_since) VALUES (9, 'frank@facebook.com', 'ivy@facebook.com', 'accepted', '2022-03-15');
INSERT INTO fb_friendships (fid, f_user1_email, f_user2_email, f_status, f_since) VALUES (10, 'grace@facebook.com', 'jack@facebook.com', 'accepted', '2022-06-01');
INSERT INTO fb_friendships (fid, f_user1_email, f_user2_email, f_status, f_since) VALUES (11, 'henry@facebook.com', 'alice@facebook.com', 'accepted', '2022-01-10');
INSERT INTO fb_friendships (fid, f_user1_email, f_user2_email, f_status, f_since) VALUES (12, 'ivy@facebook.com', 'bob@facebook.com', 'pending', '2023-04-20');
INSERT INTO fb_friendships (fid, f_user1_email, f_user2_email, f_status, f_since) VALUES (13, 'jack@facebook.com', 'carol@facebook.com', 'accepted', '2023-01-05');
INSERT INTO fb_friendships (fid, f_user1_email, f_user2_email, f_status, f_since) VALUES (14, 'dave@facebook.com', 'frank@facebook.com', 'accepted', '2022-09-12');
INSERT INTO fb_friendships (fid, f_user1_email, f_user2_email, f_status, f_since) VALUES (15, 'eve@facebook.com', 'grace@facebook.com', 'accepted', '2023-02-28');

-- =============================================
-- fb_posts (20 rows)
-- =============================================
CREATE TABLE fb_posts (
    postid INTEGER PRIMARY KEY,
    post_author_email TEXT NOT NULL,
    post_text TEXT,
    post_type TEXT DEFAULT 'text',
    post_media_url TEXT,
    post_privacy TEXT DEFAULT 'public',
    post_created TEXT,
    post_updated TEXT,
    post_likes_count INTEGER DEFAULT 0,
    post_shares_count INTEGER DEFAULT 0
);

INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (1, 'alice@facebook.com', 'Just landed in Tokyo! Amazing city vibes', 'photo', '/media/posts/alice_tokyo.jpg', 'public', '2024-01-15', '2024-01-15', 12, 3);
INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (2, 'alice@facebook.com', 'New coding project launched today @bob_rivera check it out', 'text', NULL, 'public', '2024-02-20', '2024-02-20', 8, 1);
INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (3, 'bob@facebook.com', 'Made the perfect sourdough bread today', 'photo', '/media/posts/bob_bread.jpg', 'public', '2024-01-20', '2024-01-20', 15, 2);
INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (4, 'bob@facebook.com', 'Concert night with @eve_thompson', 'photo', '/media/posts/bob_concert.jpg', 'friends', '2024-03-10', '2024-03-10', 6, 0);
INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (5, 'carol@facebook.com', 'Exploring the streets of Barcelona', 'video', '/media/posts/carol_barcelona.mp4', 'public', '2024-02-05', '2024-02-05', 20, 5);
INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (6, 'carol@facebook.com', 'Best hiking trail I have ever been on', 'photo', '/media/posts/carol_hiking.jpg', 'public', '2024-04-12', '2024-04-12', 10, 1);
INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (7, 'dave@facebook.com', 'Morning workout routine - 5am club', 'video', '/media/posts/dave_workout.mp4', 'public', '2024-01-25', '2024-01-25', 9, 2);
INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (8, 'dave@facebook.com', 'Mountain biking in Colorado', 'photo', '/media/posts/dave_biking.jpg', 'public', '2024-03-18', '2024-03-18', 14, 3);
INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (9, 'eve@facebook.com', 'New digital art piece - Neon Dreams', 'photo', '/media/posts/eve_neon.jpg', 'public', '2024-02-10', '2024-02-10', 22, 4);
INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (10, 'eve@facebook.com', 'Design tips for beginners thread', 'text', NULL, 'public', '2024-04-01', '2024-04-02', 18, 6);
INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (11, 'frank@facebook.com', 'Startup lessons learned this year', 'text', NULL, 'public', '2024-01-30', '2024-01-30', 11, 2);
INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (12, 'frank@facebook.com', 'Team building event at the office', 'photo', '/media/posts/frank_team.jpg', 'friends', '2024-03-25', '2024-03-25', 7, 0);
INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (13, 'grace@facebook.com', 'Just watched the new Nolan film - mind blown', 'text', NULL, 'public', '2024-02-15', '2024-02-15', 16, 3);
INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (14, 'grace@facebook.com', 'Oscar predictions for this year', 'link', 'https://gracereviewsblog.com/oscars', 'public', '2024-04-05', '2024-04-05', 13, 2);
INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (15, 'henry@facebook.com', 'Data visualization of climate trends', 'photo', '/media/posts/henry_dataviz.jpg', 'public', '2024-02-28', '2024-02-28', 19, 4);
INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (16, 'henry@facebook.com', 'Gaming session highlights', 'video', '/media/posts/henry_gaming.mp4', 'friends', '2024-03-30', '2024-03-30', 5, 0);
INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (17, 'ivy@facebook.com', 'Sunrise yoga on the beach', 'photo', '/media/posts/ivy_yoga.jpg', 'public', '2024-03-01', '2024-03-01', 25, 5);
INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (18, 'ivy@facebook.com', 'Wellness tips for a balanced life', 'text', NULL, 'public', '2024-04-10', '2024-04-10', 14, 2);
INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (19, 'jack@facebook.com', 'New song out now - listen on all platforms', 'link', 'https://music.example.com/jack_newsong', 'public', '2024-03-05', '2024-03-05', 21, 7);
INSERT INTO fb_posts (postid, post_author_email, post_text, post_type, post_media_url, post_privacy, post_created, post_updated, post_likes_count, post_shares_count) VALUES (20, 'jack@facebook.com', 'Behind the scenes of the recording studio', 'video', '/media/posts/jack_studio.mp4', 'public', '2024-04-15', '2024-04-15', 17, 3);

-- =============================================
-- fb_comments (25 rows)
-- =============================================
CREATE TABLE fb_comments (
    cmtid INTEGER PRIMARY KEY,
    cmt_post_id INTEGER NOT NULL,
    cmt_author_email TEXT NOT NULL,
    cmt_text TEXT NOT NULL,
    cmt_created TEXT,
    cmt_parent_id INTEGER
);

INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (1, 1, 'bob@facebook.com', 'Looks amazing! Enjoy your trip!', '2024-01-15', NULL);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (2, 1, 'carol@facebook.com', 'I love Tokyo! Try the ramen at Ichiran', '2024-01-15', NULL);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (3, 1, 'alice@facebook.com', 'Thanks Carol! Will definitely check it out', '2024-01-16', 2);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (4, 3, 'alice@facebook.com', 'That bread looks incredible!', '2024-01-20', NULL);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (5, 3, 'eve@facebook.com', 'Recipe please!', '2024-01-21', NULL);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (6, 3, 'bob@facebook.com', 'Thanks! Will share the recipe soon', '2024-01-21', 5);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (7, 5, 'alice@facebook.com', 'Barcelona is on my bucket list!', '2024-02-05', NULL);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (8, 5, 'dave@facebook.com', 'Beautiful footage Carol!', '2024-02-06', NULL);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (9, 7, 'frank@facebook.com', 'That is dedication! How do you wake up so early?', '2024-01-25', NULL);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (10, 7, 'dave@facebook.com', 'Discipline and a good alarm clock!', '2024-01-26', 9);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (11, 9, 'grace@facebook.com', 'This is stunning! What software do you use?', '2024-02-10', NULL);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (12, 9, 'eve@facebook.com', 'I use Procreate and Photoshop combo', '2024-02-11', 11);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (13, 11, 'henry@facebook.com', 'Great insights! Very relatable', '2024-01-30', NULL);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (14, 13, 'jack@facebook.com', 'Nolan never disappoints', '2024-02-15', NULL);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (15, 13, 'alice@facebook.com', 'Need to watch this ASAP', '2024-02-16', NULL);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (16, 15, 'carol@facebook.com', 'Important work Henry, thanks for sharing', '2024-02-28', NULL);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (17, 15, 'frank@facebook.com', 'Eye opening visualization', '2024-03-01', NULL);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (18, 17, 'alice@facebook.com', 'This is so peaceful!', '2024-03-01', NULL);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (19, 17, 'eve@facebook.com', 'I need to try beach yoga', '2024-03-02', NULL);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (20, 19, 'bob@facebook.com', 'Fire track! On repeat all day', '2024-03-05', NULL);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (21, 19, 'grace@facebook.com', 'Your best work yet Jack!', '2024-03-06', NULL);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (22, 19, 'jack@facebook.com', 'Thanks Grace! Means a lot', '2024-03-06', 21);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (23, 10, 'ivy@facebook.com', 'Super helpful thread Eve!', '2024-04-01', NULL);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (24, 8, 'henry@facebook.com', 'Colorado has the best trails', '2024-03-18', NULL);
INSERT INTO fb_comments (cmtid, cmt_post_id, cmt_author_email, cmt_text, cmt_created, cmt_parent_id) VALUES (25, 20, 'ivy@facebook.com', 'Love the behind the scenes content!', '2024-04-15', NULL);

-- =============================================
-- fb_likes (30 rows)
-- =============================================
CREATE TABLE fb_likes (
    likeid INTEGER PRIMARY KEY,
    like_user_email TEXT NOT NULL,
    like_target_type TEXT NOT NULL,
    like_target_id INTEGER NOT NULL,
    like_created TEXT
);

INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (1, 'bob@facebook.com', 'post', 1, '2024-01-15');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (2, 'carol@facebook.com', 'post', 1, '2024-01-15');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (3, 'dave@facebook.com', 'post', 1, '2024-01-16');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (4, 'alice@facebook.com', 'post', 3, '2024-01-20');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (5, 'eve@facebook.com', 'post', 3, '2024-01-21');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (6, 'carol@facebook.com', 'post', 5, '2024-02-05');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (7, 'alice@facebook.com', 'post', 5, '2024-02-06');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (8, 'frank@facebook.com', 'post', 7, '2024-01-25');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (9, 'grace@facebook.com', 'post', 9, '2024-02-10');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (10, 'henry@facebook.com', 'post', 9, '2024-02-11');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (11, 'jack@facebook.com', 'post', 11, '2024-01-30');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (12, 'alice@facebook.com', 'post', 13, '2024-02-15');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (13, 'carol@facebook.com', 'post', 15, '2024-02-28');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (14, 'bob@facebook.com', 'post', 17, '2024-03-01');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (15, 'eve@facebook.com', 'post', 17, '2024-03-02');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (16, 'grace@facebook.com', 'post', 19, '2024-03-05');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (17, 'henry@facebook.com', 'post', 19, '2024-03-06');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (18, 'ivy@facebook.com', 'post', 20, '2024-04-15');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (19, 'bob@facebook.com', 'comment', 1, '2024-01-15');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (20, 'alice@facebook.com', 'comment', 2, '2024-01-16');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (21, 'carol@facebook.com', 'comment', 4, '2024-01-21');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (22, 'dave@facebook.com', 'comment', 7, '2024-02-06');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (23, 'frank@facebook.com', 'comment', 9, '2024-01-26');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (24, 'grace@facebook.com', 'comment', 11, '2024-02-11');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (25, 'henry@facebook.com', 'comment', 13, '2024-01-31');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (26, 'jack@facebook.com', 'comment', 14, '2024-02-16');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (27, 'alice@facebook.com', 'comment', 18, '2024-03-02');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (28, 'eve@facebook.com', 'comment', 20, '2024-03-06');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (29, 'ivy@facebook.com', 'comment', 21, '2024-03-07');
INSERT INTO fb_likes (likeid, like_user_email, like_target_type, like_target_id, like_created) VALUES (30, 'frank@facebook.com', 'comment', 25, '2024-04-16');

-- =============================================
-- fb_photos (15 rows)
-- =============================================
CREATE TABLE fb_photos (
    phid INTEGER PRIMARY KEY,
    ph_owner_email TEXT NOT NULL,
    ph_album_name TEXT,
    ph_url TEXT NOT NULL,
    ph_caption TEXT,
    ph_tags TEXT,
    ph_uploaded TEXT
);

INSERT INTO fb_photos (phid, ph_owner_email, ph_album_name, ph_url, ph_caption, ph_tags, ph_uploaded) VALUES (1, 'alice@facebook.com', 'Travel 2024', '/photos/alice_tokyo1.jpg', 'Tokyo Tower at sunset', 'tokyo,travel', '2024-01-15');
INSERT INTO fb_photos (phid, ph_owner_email, ph_album_name, ph_url, ph_caption, ph_tags, ph_uploaded) VALUES (2, 'alice@facebook.com', 'Travel 2024', '/photos/alice_tokyo2.jpg', 'Shibuya crossing', 'tokyo,travel', '2024-01-16');
INSERT INTO fb_photos (phid, ph_owner_email, ph_album_name, ph_url, ph_caption, ph_tags, ph_uploaded) VALUES (3, 'bob@facebook.com', 'Food Adventures', '/photos/bob_bread1.jpg', 'Sourdough perfection', 'bread,baking', '2024-01-20');
INSERT INTO fb_photos (phid, ph_owner_email, ph_album_name, ph_url, ph_caption, ph_tags, ph_uploaded) VALUES (4, 'bob@facebook.com', 'Food Adventures', '/photos/bob_pasta.jpg', 'Homemade pasta night', 'pasta,cooking', '2024-02-10');
INSERT INTO fb_photos (phid, ph_owner_email, ph_album_name, ph_url, ph_caption, ph_tags, ph_uploaded) VALUES (5, 'carol@facebook.com', 'Wanderlust', '/photos/carol_barca1.jpg', 'La Sagrada Familia', 'barcelona,architecture', '2024-02-05');
INSERT INTO fb_photos (phid, ph_owner_email, ph_album_name, ph_url, ph_caption, ph_tags, ph_uploaded) VALUES (6, 'carol@facebook.com', 'Wanderlust', '/photos/carol_hiking1.jpg', 'Summit view', 'hiking,nature', '2024-04-12');
INSERT INTO fb_photos (phid, ph_owner_email, ph_album_name, ph_url, ph_caption, ph_tags, ph_uploaded) VALUES (7, 'dave@facebook.com', 'Fitness Journey', '/photos/dave_gym1.jpg', 'Leg day done', 'fitness,gym', '2024-01-25');
INSERT INTO fb_photos (phid, ph_owner_email, ph_album_name, ph_url, ph_caption, ph_tags, ph_uploaded) VALUES (8, 'dave@facebook.com', 'Fitness Journey', '/photos/dave_bike1.jpg', 'Trail riding', 'biking,outdoors', '2024-03-18');
INSERT INTO fb_photos (phid, ph_owner_email, ph_album_name, ph_url, ph_caption, ph_tags, ph_uploaded) VALUES (9, 'eve@facebook.com', 'My Art', '/photos/eve_neon1.jpg', 'Neon Dreams close-up', 'art,digital', '2024-02-10');
INSERT INTO fb_photos (phid, ph_owner_email, ph_album_name, ph_url, ph_caption, ph_tags, ph_uploaded) VALUES (10, 'eve@facebook.com', 'My Art', '/photos/eve_abstract.jpg', 'Abstract waves', 'art,abstract', '2024-03-15');
INSERT INTO fb_photos (phid, ph_owner_email, ph_album_name, ph_url, ph_caption, ph_tags, ph_uploaded) VALUES (11, 'grace@facebook.com', 'Movie Nights', '/photos/grace_cinema1.jpg', 'Film festival entrance', 'cinema,films', '2024-02-15');
INSERT INTO fb_photos (phid, ph_owner_email, ph_album_name, ph_url, ph_caption, ph_tags, ph_uploaded) VALUES (12, 'henry@facebook.com', 'Data & Code', '/photos/henry_dataviz1.jpg', 'Climate data chart', 'data,visualization', '2024-02-28');
INSERT INTO fb_photos (phid, ph_owner_email, ph_album_name, ph_url, ph_caption, ph_tags, ph_uploaded) VALUES (13, 'ivy@facebook.com', 'Yoga Life', '/photos/ivy_beach_yoga.jpg', 'Morning practice', 'yoga,beach', '2024-03-01');
INSERT INTO fb_photos (phid, ph_owner_email, ph_album_name, ph_url, ph_caption, ph_tags, ph_uploaded) VALUES (14, 'jack@facebook.com', 'Music Studio', '/photos/jack_guitar1.jpg', 'New guitar day', 'music,guitar', '2024-03-05');
INSERT INTO fb_photos (phid, ph_owner_email, ph_album_name, ph_url, ph_caption, ph_tags, ph_uploaded) VALUES (15, 'jack@facebook.com', 'Music Studio', '/photos/jack_studio1.jpg', 'Recording session', 'music,studio', '2024-04-15');

-- =============================================
-- fb_albums (8 rows)
-- =============================================
CREATE TABLE fb_albums (
    albid INTEGER PRIMARY KEY,
    alb_owner_email TEXT NOT NULL,
    alb_name TEXT NOT NULL,
    alb_desc TEXT,
    alb_privacy TEXT DEFAULT 'public',
    alb_created TEXT,
    alb_cover_url TEXT
);

INSERT INTO fb_albums (albid, alb_owner_email, alb_name, alb_desc, alb_privacy, alb_created, alb_cover_url) VALUES (1, 'alice@facebook.com', 'Travel 2024', 'Photos from my travels in 2024', 'public', '2024-01-10', '/photos/alice_tokyo1.jpg');
INSERT INTO fb_albums (albid, alb_owner_email, alb_name, alb_desc, alb_privacy, alb_created, alb_cover_url) VALUES (2, 'bob@facebook.com', 'Food Adventures', 'My culinary creations', 'public', '2024-01-15', '/photos/bob_bread1.jpg');
INSERT INTO fb_albums (albid, alb_owner_email, alb_name, alb_desc, alb_privacy, alb_created, alb_cover_url) VALUES (3, 'carol@facebook.com', 'Wanderlust', 'Places I have explored', 'public', '2024-01-20', '/photos/carol_barca1.jpg');
INSERT INTO fb_albums (albid, alb_owner_email, alb_name, alb_desc, alb_privacy, alb_created, alb_cover_url) VALUES (4, 'dave@facebook.com', 'Fitness Journey', 'Workout and outdoor photos', 'friends', '2024-01-22', '/photos/dave_gym1.jpg');
INSERT INTO fb_albums (albid, alb_owner_email, alb_name, alb_desc, alb_privacy, alb_created, alb_cover_url) VALUES (5, 'eve@facebook.com', 'My Art', 'Digital art portfolio', 'public', '2024-02-01', '/photos/eve_neon1.jpg');
INSERT INTO fb_albums (albid, alb_owner_email, alb_name, alb_desc, alb_privacy, alb_created, alb_cover_url) VALUES (6, 'grace@facebook.com', 'Movie Nights', 'Cinema and film events', 'public', '2024-02-10', '/photos/grace_cinema1.jpg');
INSERT INTO fb_albums (albid, alb_owner_email, alb_name, alb_desc, alb_privacy, alb_created, alb_cover_url) VALUES (7, 'henry@facebook.com', 'Data & Code', 'Visualizations and projects', 'private', '2024-02-20', '/photos/henry_dataviz1.jpg');
INSERT INTO fb_albums (albid, alb_owner_email, alb_name, alb_desc, alb_privacy, alb_created, alb_cover_url) VALUES (8, 'jack@facebook.com', 'Music Studio', 'Studio life and instruments', 'public', '2024-03-01', '/photos/jack_guitar1.jpg');

-- =============================================
-- fb_groups (6 rows)
-- =============================================
CREATE TABLE fb_groups (
    gid INTEGER PRIMARY KEY,
    g_name TEXT NOT NULL,
    g_desc TEXT,
    g_creator_email TEXT NOT NULL,
    g_privacy TEXT DEFAULT 'public',
    g_created TEXT,
    g_member_count INTEGER DEFAULT 0
);

INSERT INTO fb_groups (gid, g_name, g_desc, g_creator_email, g_privacy, g_created, g_member_count) VALUES (1, 'Tech Enthusiasts', 'A community for technology lovers', 'alice@facebook.com', 'public', '2021-03-01', 5);
INSERT INTO fb_groups (gid, g_name, g_desc, g_creator_email, g_privacy, g_created, g_member_count) VALUES (2, 'Foodies United', 'Share your favorite recipes and restaurants', 'bob@facebook.com', 'public', '2021-06-15', 4);
INSERT INTO fb_groups (gid, g_name, g_desc, g_creator_email, g_privacy, g_created, g_member_count) VALUES (3, 'Travel Bugs', 'For passionate travelers sharing experiences', 'carol@facebook.com', 'public', '2021-09-10', 3);
INSERT INTO fb_groups (gid, g_name, g_desc, g_creator_email, g_privacy, g_created, g_member_count) VALUES (4, 'Fitness Warriors', 'Workout tips and motivation', 'dave@facebook.com', 'private', '2022-01-05', 3);
INSERT INTO fb_groups (gid, g_name, g_desc, g_creator_email, g_privacy, g_created, g_member_count) VALUES (5, 'Creative Arts', 'Digital art, design, and photography', 'eve@facebook.com', 'public', '2022-04-20', 2);
INSERT INTO fb_groups (gid, g_name, g_desc, g_creator_email, g_privacy, g_created, g_member_count) VALUES (6, 'Music Makers', 'Musicians and songwriters connect here', 'jack@facebook.com', 'public', '2022-08-01', 1);

-- =============================================
-- fb_group_members (18 rows)
-- =============================================
CREATE TABLE fb_group_members (
    gmid INTEGER PRIMARY KEY,
    gm_group_name TEXT NOT NULL,
    gm_user_email TEXT NOT NULL,
    gm_role TEXT DEFAULT 'member',
    gm_joined TEXT
);

INSERT INTO fb_group_members (gmid, gm_group_name, gm_user_email, gm_role, gm_joined) VALUES (1, 'Tech Enthusiasts', 'alice@facebook.com', 'admin', '2021-03-01');
INSERT INTO fb_group_members (gmid, gm_group_name, gm_user_email, gm_role, gm_joined) VALUES (2, 'Tech Enthusiasts', 'henry@facebook.com', 'moderator', '2021-03-15');
INSERT INTO fb_group_members (gmid, gm_group_name, gm_user_email, gm_role, gm_joined) VALUES (3, 'Tech Enthusiasts', 'frank@facebook.com', 'member', '2021-04-01');
INSERT INTO fb_group_members (gmid, gm_group_name, gm_user_email, gm_role, gm_joined) VALUES (4, 'Tech Enthusiasts', 'bob@facebook.com', 'member', '2021-05-10');
INSERT INTO fb_group_members (gmid, gm_group_name, gm_user_email, gm_role, gm_joined) VALUES (5, 'Tech Enthusiasts', 'grace@facebook.com', 'member', '2021-06-20');
INSERT INTO fb_group_members (gmid, gm_group_name, gm_user_email, gm_role, gm_joined) VALUES (6, 'Foodies United', 'bob@facebook.com', 'admin', '2021-06-15');
INSERT INTO fb_group_members (gmid, gm_group_name, gm_user_email, gm_role, gm_joined) VALUES (7, 'Foodies United', 'alice@facebook.com', 'member', '2021-07-01');
INSERT INTO fb_group_members (gmid, gm_group_name, gm_user_email, gm_role, gm_joined) VALUES (8, 'Foodies United', 'carol@facebook.com', 'member', '2021-07-20');
INSERT INTO fb_group_members (gmid, gm_group_name, gm_user_email, gm_role, gm_joined) VALUES (9, 'Foodies United', 'ivy@facebook.com', 'member', '2022-01-10');
INSERT INTO fb_group_members (gmid, gm_group_name, gm_user_email, gm_role, gm_joined) VALUES (10, 'Travel Bugs', 'carol@facebook.com', 'admin', '2021-09-10');
INSERT INTO fb_group_members (gmid, gm_group_name, gm_user_email, gm_role, gm_joined) VALUES (11, 'Travel Bugs', 'alice@facebook.com', 'member', '2021-10-01');
INSERT INTO fb_group_members (gmid, gm_group_name, gm_user_email, gm_role, gm_joined) VALUES (12, 'Travel Bugs', 'dave@facebook.com', 'member', '2022-02-15');
INSERT INTO fb_group_members (gmid, gm_group_name, gm_user_email, gm_role, gm_joined) VALUES (13, 'Fitness Warriors', 'dave@facebook.com', 'admin', '2022-01-05');
INSERT INTO fb_group_members (gmid, gm_group_name, gm_user_email, gm_role, gm_joined) VALUES (14, 'Fitness Warriors', 'frank@facebook.com', 'member', '2022-02-01');
INSERT INTO fb_group_members (gmid, gm_group_name, gm_user_email, gm_role, gm_joined) VALUES (15, 'Fitness Warriors', 'ivy@facebook.com', 'member', '2022-03-15');
INSERT INTO fb_group_members (gmid, gm_group_name, gm_user_email, gm_role, gm_joined) VALUES (16, 'Creative Arts', 'eve@facebook.com', 'admin', '2022-04-20');
INSERT INTO fb_group_members (gmid, gm_group_name, gm_user_email, gm_role, gm_joined) VALUES (17, 'Creative Arts', 'grace@facebook.com', 'member', '2022-05-10');
INSERT INTO fb_group_members (gmid, gm_group_name, gm_user_email, gm_role, gm_joined) VALUES (18, 'Music Makers', 'jack@facebook.com', 'admin', '2022-08-01');

-- =============================================
-- fb_group_posts (12 rows)
-- =============================================
CREATE TABLE fb_group_posts (
    gpid INTEGER PRIMARY KEY,
    gp_group_name TEXT NOT NULL,
    gp_author_email TEXT NOT NULL,
    gp_text TEXT NOT NULL,
    gp_media_url TEXT,
    gp_created TEXT
);

INSERT INTO fb_group_posts (gpid, gp_group_name, gp_author_email, gp_text, gp_media_url, gp_created) VALUES (1, 'Tech Enthusiasts', 'alice@facebook.com', 'Check out this new AI framework!', 'https://example.com/ai-framework', '2024-01-10');
INSERT INTO fb_group_posts (gpid, gp_group_name, gp_author_email, gp_text, gp_media_url, gp_created) VALUES (2, 'Tech Enthusiasts', 'henry@facebook.com', 'Python 3.13 release notes discussion', NULL, '2024-02-01');
INSERT INTO fb_group_posts (gpid, gp_group_name, gp_author_email, gp_text, gp_media_url, gp_created) VALUES (3, 'Tech Enthusiasts', 'frank@facebook.com', 'Best practices for microservices architecture', NULL, '2024-03-05');
INSERT INTO fb_group_posts (gpid, gp_group_name, gp_author_email, gp_text, gp_media_url, gp_created) VALUES (4, 'Foodies United', 'bob@facebook.com', 'My secret pasta sauce recipe', '/media/group/bob_sauce.jpg', '2024-01-20');
INSERT INTO fb_group_posts (gpid, gp_group_name, gp_author_email, gp_text, gp_media_url, gp_created) VALUES (5, 'Foodies United', 'alice@facebook.com', 'Best sushi in San Francisco', NULL, '2024-02-15');
INSERT INTO fb_group_posts (gpid, gp_group_name, gp_author_email, gp_text, gp_media_url, gp_created) VALUES (6, 'Travel Bugs', 'carol@facebook.com', 'Top 10 hidden gems in Southeast Asia', '/media/group/carol_asia.jpg', '2024-02-20');
INSERT INTO fb_group_posts (gpid, gp_group_name, gp_author_email, gp_text, gp_media_url, gp_created) VALUES (7, 'Travel Bugs', 'alice@facebook.com', 'Packing tips for long trips', NULL, '2024-03-10');
INSERT INTO fb_group_posts (gpid, gp_group_name, gp_author_email, gp_text, gp_media_url, gp_created) VALUES (8, 'Fitness Warriors', 'dave@facebook.com', 'Weekly challenge: 100 push-ups daily', NULL, '2024-01-15');
INSERT INTO fb_group_posts (gpid, gp_group_name, gp_author_email, gp_text, gp_media_url, gp_created) VALUES (9, 'Fitness Warriors', 'frank@facebook.com', 'Best protein shake recipes', '/media/group/frank_shake.jpg', '2024-02-10');
INSERT INTO fb_group_posts (gpid, gp_group_name, gp_author_email, gp_text, gp_media_url, gp_created) VALUES (10, 'Creative Arts', 'eve@facebook.com', 'Free design resources for 2024', '/media/group/eve_resources.jpg', '2024-03-01');
INSERT INTO fb_group_posts (gpid, gp_group_name, gp_author_email, gp_text, gp_media_url, gp_created) VALUES (11, 'Creative Arts', 'grace@facebook.com', 'Cinematography techniques for beginners', NULL, '2024-03-20');
INSERT INTO fb_group_posts (gpid, gp_group_name, gp_author_email, gp_text, gp_media_url, gp_created) VALUES (12, 'Music Makers', 'jack@facebook.com', 'Looking for collaborators on new album', NULL, '2024-04-01');

-- =============================================
-- fb_pages (5 rows)
-- =============================================
CREATE TABLE fb_pages (
    pageid INTEGER PRIMARY KEY,
    pg_name TEXT NOT NULL,
    pg_category TEXT NOT NULL,
    pg_owner_email TEXT NOT NULL,
    pg_desc TEXT,
    pg_website TEXT,
    pg_created TEXT,
    pg_followers_count INTEGER DEFAULT 0
);

INSERT INTO fb_pages (pageid, pg_name, pg_category, pg_owner_email, pg_desc, pg_website, pg_created, pg_followers_count) VALUES (1, 'Alice Tech Blog', 'Technology', 'alice@facebook.com', 'Tech tutorials and coding tips', 'https://alicechen.dev', '2021-06-01', 3);
INSERT INTO fb_pages (pageid, pg_name, pg_category, pg_owner_email, pg_desc, pg_website, pg_created, pg_followers_count) VALUES (2, 'Bob Kitchen', 'Food & Drink', 'bob@facebook.com', 'Recipes and cooking adventures', 'https://bobkitchen.com', '2021-09-15', 2);
INSERT INTO fb_pages (pageid, pg_name, pg_category, pg_owner_email, pg_desc, pg_website, pg_created, pg_followers_count) VALUES (3, 'Carol Travels', 'Travel', 'carol@facebook.com', 'Travel guides and destination reviews', 'https://carolztravels.com', '2022-01-10', 3);
INSERT INTO fb_pages (pageid, pg_name, pg_category, pg_owner_email, pg_desc, pg_website, pg_created, pg_followers_count) VALUES (4, 'Eve Design Studio', 'Art & Design', 'eve@facebook.com', 'Digital art showcase and tutorials', 'https://evedesigns.co', '2022-05-20', 2);
INSERT INTO fb_pages (pageid, pg_name, pg_category, pg_owner_email, pg_desc, pg_website, pg_created, pg_followers_count) VALUES (5, 'Jack Music', 'Music', 'jack@facebook.com', 'Original music and live sessions', 'https://jackmurphymusic.com', '2022-09-01', 2);

-- =============================================
-- fb_page_followers (12 rows)
-- =============================================
CREATE TABLE fb_page_followers (
    pfid INTEGER PRIMARY KEY,
    pf_page_name TEXT NOT NULL,
    pf_user_email TEXT NOT NULL,
    pf_followed_since TEXT
);

INSERT INTO fb_page_followers (pfid, pf_page_name, pf_user_email, pf_followed_since) VALUES (1, 'Alice Tech Blog', 'bob@facebook.com', '2021-07-01');
INSERT INTO fb_page_followers (pfid, pf_page_name, pf_user_email, pf_followed_since) VALUES (2, 'Alice Tech Blog', 'henry@facebook.com', '2021-11-15');
INSERT INTO fb_page_followers (pfid, pf_page_name, pf_user_email, pf_followed_since) VALUES (3, 'Alice Tech Blog', 'frank@facebook.com', '2022-03-01');
INSERT INTO fb_page_followers (pfid, pf_page_name, pf_user_email, pf_followed_since) VALUES (4, 'Bob Kitchen', 'alice@facebook.com', '2021-10-01');
INSERT INTO fb_page_followers (pfid, pf_page_name, pf_user_email, pf_followed_since) VALUES (5, 'Bob Kitchen', 'carol@facebook.com', '2022-02-14');
INSERT INTO fb_page_followers (pfid, pf_page_name, pf_user_email, pf_followed_since) VALUES (6, 'Carol Travels', 'alice@facebook.com', '2022-02-01');
INSERT INTO fb_page_followers (pfid, pf_page_name, pf_user_email, pf_followed_since) VALUES (7, 'Carol Travels', 'dave@facebook.com', '2022-04-10');
INSERT INTO fb_page_followers (pfid, pf_page_name, pf_user_email, pf_followed_since) VALUES (8, 'Carol Travels', 'ivy@facebook.com', '2022-06-20');
INSERT INTO fb_page_followers (pfid, pf_page_name, pf_user_email, pf_followed_since) VALUES (9, 'Eve Design Studio', 'grace@facebook.com', '2022-06-15');
INSERT INTO fb_page_followers (pfid, pf_page_name, pf_user_email, pf_followed_since) VALUES (10, 'Eve Design Studio', 'alice@facebook.com', '2022-08-01');
INSERT INTO fb_page_followers (pfid, pf_page_name, pf_user_email, pf_followed_since) VALUES (11, 'Jack Music', 'bob@facebook.com', '2022-10-01');
INSERT INTO fb_page_followers (pfid, pf_page_name, pf_user_email, pf_followed_since) VALUES (12, 'Jack Music', 'grace@facebook.com', '2023-01-15');

-- =============================================
-- fb_conversations (8 rows)
-- =============================================
CREATE TABLE fb_conversations (
    convid INTEGER PRIMARY KEY,
    conv_user1_email TEXT NOT NULL,
    conv_user2_email TEXT NOT NULL,
    conv_created TEXT,
    conv_last_msg TEXT
);

INSERT INTO fb_conversations (convid, conv_user1_email, conv_user2_email, conv_created, conv_last_msg) VALUES (1, 'alice@facebook.com', 'bob@facebook.com', '2021-01-20', '2024-04-10');
INSERT INTO fb_conversations (convid, conv_user1_email, conv_user2_email, conv_created, conv_last_msg) VALUES (2, 'alice@facebook.com', 'carol@facebook.com', '2021-03-15', '2024-03-25');
INSERT INTO fb_conversations (convid, conv_user1_email, conv_user2_email, conv_created, conv_last_msg) VALUES (3, 'bob@facebook.com', 'eve@facebook.com', '2021-06-10', '2024-04-05');
INSERT INTO fb_conversations (convid, conv_user1_email, conv_user2_email, conv_created, conv_last_msg) VALUES (4, 'carol@facebook.com', 'dave@facebook.com', '2022-01-05', '2024-03-15');
INSERT INTO fb_conversations (convid, conv_user1_email, conv_user2_email, conv_created, conv_last_msg) VALUES (5, 'dave@facebook.com', 'frank@facebook.com', '2022-04-20', '2024-02-28');
INSERT INTO fb_conversations (convid, conv_user1_email, conv_user2_email, conv_created, conv_last_msg) VALUES (6, 'eve@facebook.com', 'grace@facebook.com', '2022-07-15', '2024-04-12');
INSERT INTO fb_conversations (convid, conv_user1_email, conv_user2_email, conv_created, conv_last_msg) VALUES (7, 'henry@facebook.com', 'ivy@facebook.com', '2023-01-10', '2024-03-20');
INSERT INTO fb_conversations (convid, conv_user1_email, conv_user2_email, conv_created, conv_last_msg) VALUES (8, 'jack@facebook.com', 'grace@facebook.com', '2023-05-01', '2024-04-08');

-- =============================================
-- fb_messages (20 rows)
-- =============================================
CREATE TABLE fb_messages (
    msgid INTEGER PRIMARY KEY,
    msg_conv_id INTEGER NOT NULL,
    msg_sender_email TEXT NOT NULL,
    msg_text TEXT,
    msg_media_url TEXT,
    msg_sent TEXT,
    msg_read TEXT
);

INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (1, 1, 'alice@facebook.com', 'Hey Bob! How is the new recipe going?', NULL, '2024-03-01', '2024-03-01');
INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (2, 1, 'bob@facebook.com', 'Great! Just perfected the sourdough', NULL, '2024-03-01', '2024-03-02');
INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (3, 1, 'alice@facebook.com', 'Send me photos!', NULL, '2024-04-10', '2024-04-10');
INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (4, 2, 'alice@facebook.com', 'Carol, want to plan a trip together?', NULL, '2024-02-20', '2024-02-20');
INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (5, 2, 'carol@facebook.com', 'Yes! I was thinking about Japan', NULL, '2024-02-21', '2024-02-21');
INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (6, 2, 'alice@facebook.com', 'Perfect! Let me send you my itinerary', '/media/msg/alice_itinerary.pdf', '2024-03-25', '2024-03-25');
INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (7, 3, 'bob@facebook.com', 'Eve, love your latest artwork!', NULL, '2024-03-15', '2024-03-15');
INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (8, 3, 'eve@facebook.com', 'Thanks Bob! Working on a new series', NULL, '2024-03-16', '2024-03-16');
INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (9, 3, 'eve@facebook.com', 'Here is a sneak peek', '/media/msg/eve_preview.jpg', '2024-04-05', '2024-04-05');
INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (10, 4, 'carol@facebook.com', 'Dave, any trail recommendations?', NULL, '2024-02-10', '2024-02-10');
INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (11, 4, 'dave@facebook.com', 'Check out the Maroon Bells loop!', NULL, '2024-02-11', '2024-02-11');
INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (12, 4, 'carol@facebook.com', 'Added to my list!', NULL, '2024-03-15', '2024-03-15');
INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (13, 5, 'dave@facebook.com', 'Frank, want to hit the gym Saturday?', NULL, '2024-02-15', '2024-02-15');
INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (14, 5, 'frank@facebook.com', 'Count me in! 8am?', NULL, '2024-02-15', '2024-02-16');
INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (15, 5, 'dave@facebook.com', 'Perfect, see you there', NULL, '2024-02-28', '2024-02-28');
INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (16, 6, 'eve@facebook.com', 'Grace, have you seen the new Villeneuve film?', NULL, '2024-03-20', '2024-03-20');
INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (17, 6, 'grace@facebook.com', 'Not yet! Want to go this weekend?', NULL, '2024-03-21', '2024-03-21');
INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (18, 7, 'henry@facebook.com', 'Ivy, any meditation app recommendations?', NULL, '2024-03-10', '2024-03-10');
INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (19, 7, 'ivy@facebook.com', 'Try Headspace or Calm - both are great!', NULL, '2024-03-20', '2024-03-20');
INSERT INTO fb_messages (msgid, msg_conv_id, msg_sender_email, msg_text, msg_media_url, msg_sent, msg_read) VALUES (20, 8, 'jack@facebook.com', 'Grace, want to review my new track?', '/media/msg/jack_demo.mp3', '2024-04-08', NULL);

-- =============================================
-- fb_events (6 rows)
-- =============================================
CREATE TABLE fb_events (
    evid INTEGER PRIMARY KEY,
    ev_name TEXT NOT NULL,
    ev_creator_email TEXT NOT NULL,
    ev_desc TEXT,
    ev_location TEXT,
    ev_start TEXT,
    ev_end TEXT,
    ev_privacy TEXT DEFAULT 'public',
    ev_created TEXT
);

INSERT INTO fb_events (evid, ev_name, ev_creator_email, ev_desc, ev_location, ev_start, ev_end, ev_privacy, ev_created) VALUES (1, 'Tech Meetup 2024', 'alice@facebook.com', 'Monthly technology meetup and networking', 'San Francisco Convention Center', '2024-03-15 18:00', '2024-03-15 21:00', 'public', '2024-02-01');
INSERT INTO fb_events (evid, ev_name, ev_creator_email, ev_desc, ev_location, ev_start, ev_end, ev_privacy, ev_created) VALUES (2, 'Cooking Workshop', 'bob@facebook.com', 'Learn to make authentic Italian pasta', 'Community Kitchen Austin', '2024-04-10 14:00', '2024-04-10 17:00', 'public', '2024-03-01');
INSERT INTO fb_events (evid, ev_name, ev_creator_email, ev_desc, ev_location, ev_start, ev_end, ev_privacy, ev_created) VALUES (3, 'Photo Walk', 'carol@facebook.com', 'Street photography walk through downtown', 'Pike Place Market Seattle', '2024-04-20 10:00', '2024-04-20 13:00', 'public', '2024-03-10');
INSERT INTO fb_events (evid, ev_name, ev_creator_email, ev_desc, ev_location, ev_start, ev_end, ev_privacy, ev_created) VALUES (4, 'Fitness Bootcamp', 'dave@facebook.com', 'High intensity outdoor workout', 'City Park Denver', '2024-05-01 06:00', '2024-05-01 08:00', 'private', '2024-03-20');
INSERT INTO fb_events (evid, ev_name, ev_creator_email, ev_desc, ev_location, ev_start, ev_end, ev_privacy, ev_created) VALUES (5, 'Art Exhibition Opening', 'eve@facebook.com', 'Digital art exhibition featuring local artists', 'Miami Art Gallery', '2024-05-15 19:00', '2024-05-15 22:00', 'public', '2024-04-01');
INSERT INTO fb_events (evid, ev_name, ev_creator_email, ev_desc, ev_location, ev_start, ev_end, ev_privacy, ev_created) VALUES (6, 'Live Music Night', 'jack@facebook.com', 'Acoustic live performance', 'Nashville Music Hall', '2024-06-01 20:00', '2024-06-01 23:00', 'public', '2024-04-15');

-- =============================================
-- fb_event_rsvps (15 rows)
-- =============================================
CREATE TABLE fb_event_rsvps (
    rsvpid INTEGER PRIMARY KEY,
    rsvp_event_name TEXT NOT NULL,
    rsvp_user_email TEXT NOT NULL,
    rsvp_status TEXT DEFAULT 'going',
    rsvp_created TEXT
);

INSERT INTO fb_event_rsvps (rsvpid, rsvp_event_name, rsvp_user_email, rsvp_status, rsvp_created) VALUES (1, 'Tech Meetup 2024', 'alice@facebook.com', 'going', '2024-02-05');
INSERT INTO fb_event_rsvps (rsvpid, rsvp_event_name, rsvp_user_email, rsvp_status, rsvp_created) VALUES (2, 'Tech Meetup 2024', 'henry@facebook.com', 'going', '2024-02-10');
INSERT INTO fb_event_rsvps (rsvpid, rsvp_event_name, rsvp_user_email, rsvp_status, rsvp_created) VALUES (3, 'Tech Meetup 2024', 'frank@facebook.com', 'maybe', '2024-02-12');
INSERT INTO fb_event_rsvps (rsvpid, rsvp_event_name, rsvp_user_email, rsvp_status, rsvp_created) VALUES (4, 'Cooking Workshop', 'bob@facebook.com', 'going', '2024-03-05');
INSERT INTO fb_event_rsvps (rsvpid, rsvp_event_name, rsvp_user_email, rsvp_status, rsvp_created) VALUES (5, 'Cooking Workshop', 'alice@facebook.com', 'going', '2024-03-10');
INSERT INTO fb_event_rsvps (rsvpid, rsvp_event_name, rsvp_user_email, rsvp_status, rsvp_created) VALUES (6, 'Cooking Workshop', 'carol@facebook.com', 'interested', '2024-03-12');
INSERT INTO fb_event_rsvps (rsvpid, rsvp_event_name, rsvp_user_email, rsvp_status, rsvp_created) VALUES (7, 'Photo Walk', 'carol@facebook.com', 'going', '2024-03-15');
INSERT INTO fb_event_rsvps (rsvpid, rsvp_event_name, rsvp_user_email, rsvp_status, rsvp_created) VALUES (8, 'Photo Walk', 'alice@facebook.com', 'interested', '2024-03-18');
INSERT INTO fb_event_rsvps (rsvpid, rsvp_event_name, rsvp_user_email, rsvp_status, rsvp_created) VALUES (9, 'Fitness Bootcamp', 'dave@facebook.com', 'going', '2024-03-25');
INSERT INTO fb_event_rsvps (rsvpid, rsvp_event_name, rsvp_user_email, rsvp_status, rsvp_created) VALUES (10, 'Fitness Bootcamp', 'frank@facebook.com', 'going', '2024-03-28');
INSERT INTO fb_event_rsvps (rsvpid, rsvp_event_name, rsvp_user_email, rsvp_status, rsvp_created) VALUES (11, 'Art Exhibition Opening', 'eve@facebook.com', 'going', '2024-04-05');
INSERT INTO fb_event_rsvps (rsvpid, rsvp_event_name, rsvp_user_email, rsvp_status, rsvp_created) VALUES (12, 'Art Exhibition Opening', 'grace@facebook.com', 'going', '2024-04-08');
INSERT INTO fb_event_rsvps (rsvpid, rsvp_event_name, rsvp_user_email, rsvp_status, rsvp_created) VALUES (13, 'Art Exhibition Opening', 'alice@facebook.com', 'maybe', '2024-04-10');
INSERT INTO fb_event_rsvps (rsvpid, rsvp_event_name, rsvp_user_email, rsvp_status, rsvp_created) VALUES (14, 'Live Music Night', 'jack@facebook.com', 'going', '2024-04-20');
INSERT INTO fb_event_rsvps (rsvpid, rsvp_event_name, rsvp_user_email, rsvp_status, rsvp_created) VALUES (15, 'Live Music Night', 'bob@facebook.com', 'going', '2024-04-25');

-- =============================================
-- fb_notifications (20 rows)
-- =============================================
CREATE TABLE fb_notifications (
    notifid INTEGER PRIMARY KEY,
    notif_user_email TEXT NOT NULL,
    notif_type TEXT NOT NULL,
    notif_text TEXT,
    notif_read INTEGER DEFAULT 0,
    notif_created TEXT,
    notif_source_id INTEGER
);

INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (1, 'alice@facebook.com', 'like', 'Bob liked your post', 1, '2024-01-15', 1);
INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (2, 'alice@facebook.com', 'comment', 'Carol commented on your post', 1, '2024-01-15', 2);
INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (3, 'bob@facebook.com', 'like', 'Alice liked your post', 1, '2024-01-20', 4);
INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (4, 'carol@facebook.com', 'comment', 'Alice commented on your post', 1, '2024-02-05', 7);
INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (5, 'dave@facebook.com', 'like', 'Frank liked your post', 1, '2024-01-25', 8);
INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (6, 'eve@facebook.com', 'like', 'Grace liked your post', 0, '2024-02-10', 9);
INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (7, 'eve@facebook.com', 'comment', 'Grace commented on your art', 1, '2024-02-10', 11);
INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (8, 'frank@facebook.com', 'like', 'Jack liked your post', 0, '2024-01-30', 11);
INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (9, 'grace@facebook.com', 'like', 'Alice liked your post', 1, '2024-02-15', 12);
INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (10, 'henry@facebook.com', 'comment', 'Carol commented on your post', 1, '2024-02-28', 16);
INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (11, 'ivy@facebook.com', 'like', 'Bob liked your post', 0, '2024-03-01', 14);
INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (12, 'ivy@facebook.com', 'comment', 'Alice commented on your post', 1, '2024-03-01', 18);
INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (13, 'jack@facebook.com', 'like', 'Grace liked your post', 1, '2024-03-05', 16);
INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (14, 'jack@facebook.com', 'comment', 'Bob commented on your song post', 0, '2024-03-05', 20);
INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (15, 'alice@facebook.com', 'friend_request', 'Henry sent you a friend request', 1, '2022-01-10', NULL);
INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (16, 'bob@facebook.com', 'event', 'You are invited to Cooking Workshop', 0, '2024-03-01', 2);
INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (17, 'carol@facebook.com', 'group', 'New post in Travel Bugs', 1, '2024-03-10', 7);
INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (18, 'dave@facebook.com', 'friend_request', 'Eve wants to connect', 0, '2023-06-15', NULL);
INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (19, 'eve@facebook.com', 'page', 'Your page Eve Design Studio got a new follower', 1, '2022-08-01', 4);
INSERT INTO fb_notifications (notifid, notif_user_email, notif_type, notif_text, notif_read, notif_created, notif_source_id) VALUES (20, 'frank@facebook.com', 'group', 'New post in Tech Enthusiasts', 0, '2024-03-05', 3);

-- =============================================
-- fb_activity_log (15 rows)
-- =============================================
CREATE TABLE fb_activity_log (
    actid INTEGER PRIMARY KEY,
    act_user_email TEXT NOT NULL,
    act_type TEXT NOT NULL,
    act_detail TEXT,
    act_target_type TEXT,
    act_target_id INTEGER,
    act_created TEXT
);

INSERT INTO fb_activity_log (actid, act_user_email, act_type, act_detail, act_target_type, act_target_id, act_created) VALUES (1, 'alice@facebook.com', 'login', 'Logged in from Chrome on macOS', 'session', NULL, '2024-04-10');
INSERT INTO fb_activity_log (actid, act_user_email, act_type, act_detail, act_target_type, act_target_id, act_created) VALUES (2, 'alice@facebook.com', 'post_create', 'Created a new photo post', 'post', 1, '2024-01-15');
INSERT INTO fb_activity_log (actid, act_user_email, act_type, act_detail, act_target_type, act_target_id, act_created) VALUES (3, 'bob@facebook.com', 'login', 'Logged in from Safari on iOS', 'session', NULL, '2024-04-08');
INSERT INTO fb_activity_log (actid, act_user_email, act_type, act_detail, act_target_type, act_target_id, act_created) VALUES (4, 'bob@facebook.com', 'post_create', 'Created a new photo post', 'post', 3, '2024-01-20');
INSERT INTO fb_activity_log (actid, act_user_email, act_type, act_detail, act_target_type, act_target_id, act_created) VALUES (5, 'carol@facebook.com', 'login', 'Logged in from Firefox on Windows', 'session', NULL, '2024-04-05');
INSERT INTO fb_activity_log (actid, act_user_email, act_type, act_detail, act_target_type, act_target_id, act_created) VALUES (6, 'carol@facebook.com', 'profile_update', 'Updated bio and avatar', 'profile', 3, '2024-03-20');
INSERT INTO fb_activity_log (actid, act_user_email, act_type, act_detail, act_target_type, act_target_id, act_created) VALUES (7, 'dave@facebook.com', 'login', 'Logged in from Chrome on Android', 'session', NULL, '2024-04-01');
INSERT INTO fb_activity_log (actid, act_user_email, act_type, act_detail, act_target_type, act_target_id, act_created) VALUES (8, 'eve@facebook.com', 'post_create', 'Created a new art post', 'post', 9, '2024-02-10');
INSERT INTO fb_activity_log (actid, act_user_email, act_type, act_detail, act_target_type, act_target_id, act_created) VALUES (9, 'frank@facebook.com', 'login', 'Logged in from Edge on Windows', 'session', NULL, '2024-03-28');
INSERT INTO fb_activity_log (actid, act_user_email, act_type, act_detail, act_target_type, act_target_id, act_created) VALUES (10, 'grace@facebook.com', 'post_create', 'Created a new text post', 'post', 13, '2024-02-15');
INSERT INTO fb_activity_log (actid, act_user_email, act_type, act_detail, act_target_type, act_target_id, act_created) VALUES (11, 'henry@facebook.com', 'login', 'Logged in from Chrome on macOS', 'session', NULL, '2024-03-25');
INSERT INTO fb_activity_log (actid, act_user_email, act_type, act_detail, act_target_type, act_target_id, act_created) VALUES (12, 'ivy@facebook.com', 'post_create', 'Created a new photo post', 'post', 17, '2024-03-01');
INSERT INTO fb_activity_log (actid, act_user_email, act_type, act_detail, act_target_type, act_target_id, act_created) VALUES (13, 'jack@facebook.com', 'login', 'Logged in from Safari on macOS', 'session', NULL, '2024-04-12');
INSERT INTO fb_activity_log (actid, act_user_email, act_type, act_detail, act_target_type, act_target_id, act_created) VALUES (14, 'jack@facebook.com', 'post_create', 'Created a new link post', 'post', 19, '2024-03-05');
INSERT INTO fb_activity_log (actid, act_user_email, act_type, act_detail, act_target_type, act_target_id, act_created) VALUES (15, 'alice@facebook.com', 'settings_change', 'Updated privacy settings', 'settings', NULL, '2024-02-01');

-- =============================================
-- fb_reports (6 rows)
-- =============================================
CREATE TABLE fb_reports (
    repid INTEGER PRIMARY KEY,
    rep_reporter_email TEXT NOT NULL,
    rep_target_type TEXT NOT NULL,
    rep_target_id INTEGER NOT NULL,
    rep_reason TEXT NOT NULL,
    rep_status TEXT DEFAULT 'pending',
    rep_created TEXT
);

INSERT INTO fb_reports (repid, rep_reporter_email, rep_target_type, rep_target_id, rep_reason, rep_status, rep_created) VALUES (1, 'alice@facebook.com', 'post', 16, 'Inappropriate content', 'reviewed', '2024-04-01');
INSERT INTO fb_reports (repid, rep_reporter_email, rep_target_type, rep_target_id, rep_reason, rep_status, rep_created) VALUES (2, 'bob@facebook.com', 'comment', 10, 'Spam', 'pending', '2024-02-01');
INSERT INTO fb_reports (repid, rep_reporter_email, rep_target_type, rep_target_id, rep_reason, rep_status, rep_created) VALUES (3, 'carol@facebook.com', 'post', 12, 'Misleading information', 'reviewed', '2024-03-28');
INSERT INTO fb_reports (repid, rep_reporter_email, rep_target_type, rep_target_id, rep_reason, rep_status, rep_created) VALUES (4, 'dave@facebook.com', 'comment', 6, 'Harassment', 'pending', '2024-01-25');
INSERT INTO fb_reports (repid, rep_reporter_email, rep_target_type, rep_target_id, rep_reason, rep_status, rep_created) VALUES (5, 'eve@facebook.com', 'post', 4, 'Copyright violation', 'dismissed', '2024-03-15');
INSERT INTO fb_reports (repid, rep_reporter_email, rep_target_type, rep_target_id, rep_reason, rep_status, rep_created) VALUES (6, 'frank@facebook.com', 'comment', 22, 'Hate speech', 'pending', '2024-03-10');

-- =============================================
-- fb_privacy_settings (10 rows)
-- =============================================
CREATE TABLE fb_privacy_settings (
    psid INTEGER PRIMARY KEY,
    ps_user_email TEXT NOT NULL,
    ps_profile_vis TEXT DEFAULT 'public',
    ps_post_default TEXT DEFAULT 'public',
    ps_friend_list_vis TEXT DEFAULT 'friends',
    ps_search_vis TEXT DEFAULT 'everyone',
    ps_updated TEXT
);

INSERT INTO fb_privacy_settings (psid, ps_user_email, ps_profile_vis, ps_post_default, ps_friend_list_vis, ps_search_vis, ps_updated) VALUES (1, 'alice@facebook.com', 'public', 'public', 'friends', 'everyone', '2024-02-01');
INSERT INTO fb_privacy_settings (psid, ps_user_email, ps_profile_vis, ps_post_default, ps_friend_list_vis, ps_search_vis, ps_updated) VALUES (2, 'bob@facebook.com', 'public', 'public', 'friends', 'everyone', '2023-12-15');
INSERT INTO fb_privacy_settings (psid, ps_user_email, ps_profile_vis, ps_post_default, ps_friend_list_vis, ps_search_vis, ps_updated) VALUES (3, 'carol@facebook.com', 'public', 'public', 'everyone', 'everyone', '2024-01-10');
INSERT INTO fb_privacy_settings (psid, ps_user_email, ps_profile_vis, ps_post_default, ps_friend_list_vis, ps_search_vis, ps_updated) VALUES (4, 'dave@facebook.com', 'private', 'friends', 'only_me', 'friends', '2024-03-05');
INSERT INTO fb_privacy_settings (psid, ps_user_email, ps_profile_vis, ps_post_default, ps_friend_list_vis, ps_search_vis, ps_updated) VALUES (5, 'eve@facebook.com', 'public', 'public', 'friends', 'everyone', '2023-11-20');
INSERT INTO fb_privacy_settings (psid, ps_user_email, ps_profile_vis, ps_post_default, ps_friend_list_vis, ps_search_vis, ps_updated) VALUES (6, 'frank@facebook.com', 'public', 'public', 'friends', 'everyone', '2024-01-25');
INSERT INTO fb_privacy_settings (psid, ps_user_email, ps_profile_vis, ps_post_default, ps_friend_list_vis, ps_search_vis, ps_updated) VALUES (7, 'grace@facebook.com', 'public', 'public', 'everyone', 'everyone', '2023-10-05');
INSERT INTO fb_privacy_settings (psid, ps_user_email, ps_profile_vis, ps_post_default, ps_friend_list_vis, ps_search_vis, ps_updated) VALUES (8, 'henry@facebook.com', 'private', 'friends', 'only_me', 'friends', '2024-02-20');
INSERT INTO fb_privacy_settings (psid, ps_user_email, ps_profile_vis, ps_post_default, ps_friend_list_vis, ps_search_vis, ps_updated) VALUES (9, 'ivy@facebook.com', 'public', 'public', 'friends', 'everyone', '2023-09-15');
INSERT INTO fb_privacy_settings (psid, ps_user_email, ps_profile_vis, ps_post_default, ps_friend_list_vis, ps_search_vis, ps_updated) VALUES (10, 'jack@facebook.com', 'public', 'public', 'friends', 'everyone', '2024-03-10');

-- =============================================
-- fb_blocked_users (5 rows)
-- =============================================
CREATE TABLE fb_blocked_users (
    blkid INTEGER PRIMARY KEY,
    blk_blocker_email TEXT NOT NULL,
    blk_blocked_email TEXT NOT NULL,
    blk_reason TEXT,
    blk_created TEXT
);

INSERT INTO fb_blocked_users (blkid, blk_blocker_email, blk_blocked_email, blk_reason, blk_created) VALUES (1, 'alice@facebook.com', 'jack@facebook.com', 'Spam messages', '2023-06-15');
INSERT INTO fb_blocked_users (blkid, blk_blocker_email, blk_blocked_email, blk_reason, blk_created) VALUES (2, 'bob@facebook.com', 'frank@facebook.com', 'Harassment', '2023-09-20');
INSERT INTO fb_blocked_users (blkid, blk_blocker_email, blk_blocked_email, blk_reason, blk_created) VALUES (3, 'carol@facebook.com', 'henry@facebook.com', 'Unwanted contact', '2024-01-05');
INSERT INTO fb_blocked_users (blkid, blk_blocker_email, blk_blocked_email, blk_reason, blk_created) VALUES (4, 'dave@facebook.com', 'ivy@facebook.com', 'Inappropriate content', '2024-02-10');
INSERT INTO fb_blocked_users (blkid, blk_blocker_email, blk_blocked_email, blk_reason, blk_created) VALUES (5, 'eve@facebook.com', 'bob@facebook.com', 'Privacy concerns', '2024-03-01');

-- =============================================
-- fb_saved_items (10 rows)
-- =============================================
CREATE TABLE fb_saved_items (
    savid INTEGER PRIMARY KEY,
    sav_user_email TEXT NOT NULL,
    sav_target_type TEXT NOT NULL,
    sav_target_id INTEGER NOT NULL,
    sav_created TEXT
);

INSERT INTO fb_saved_items (savid, sav_user_email, sav_target_type, sav_target_id, sav_created) VALUES (1, 'alice@facebook.com', 'post', 5, '2024-02-06');
INSERT INTO fb_saved_items (savid, sav_user_email, sav_target_type, sav_target_id, sav_created) VALUES (2, 'alice@facebook.com', 'post', 9, '2024-02-11');
INSERT INTO fb_saved_items (savid, sav_user_email, sav_target_type, sav_target_id, sav_created) VALUES (3, 'bob@facebook.com', 'post', 1, '2024-01-16');
INSERT INTO fb_saved_items (savid, sav_user_email, sav_target_type, sav_target_id, sav_created) VALUES (4, 'carol@facebook.com', 'post', 17, '2024-03-02');
INSERT INTO fb_saved_items (savid, sav_user_email, sav_target_type, sav_target_id, sav_created) VALUES (5, 'dave@facebook.com', 'post', 7, '2024-01-26');
INSERT INTO fb_saved_items (savid, sav_user_email, sav_target_type, sav_target_id, sav_created) VALUES (6, 'eve@facebook.com', 'post', 19, '2024-03-06');
INSERT INTO fb_saved_items (savid, sav_user_email, sav_target_type, sav_target_id, sav_created) VALUES (7, 'grace@facebook.com', 'post', 15, '2024-02-28');
INSERT INTO fb_saved_items (savid, sav_user_email, sav_target_type, sav_target_id, sav_created) VALUES (8, 'henry@facebook.com', 'post', 9, '2024-02-12');
INSERT INTO fb_saved_items (savid, sav_user_email, sav_target_type, sav_target_id, sav_created) VALUES (9, 'ivy@facebook.com', 'post', 3, '2024-01-22');
INSERT INTO fb_saved_items (savid, sav_user_email, sav_target_type, sav_target_id, sav_created) VALUES (10, 'jack@facebook.com', 'post', 13, '2024-02-16');

-- =============================================
-- fb_hashtags (8 rows)
-- =============================================
CREATE TABLE fb_hashtags (
    hashid INTEGER PRIMARY KEY,
    hash_tag TEXT NOT NULL,
    hash_post_count INTEGER DEFAULT 0,
    hash_created TEXT
);

INSERT INTO fb_hashtags (hashid, hash_tag, hash_post_count, hash_created) VALUES (1, 'travel', 4, '2023-01-01');
INSERT INTO fb_hashtags (hashid, hash_tag, hash_post_count, hash_created) VALUES (2, 'food', 2, '2023-01-01');
INSERT INTO fb_hashtags (hashid, hash_tag, hash_post_count, hash_created) VALUES (3, 'fitness', 3, '2023-02-01');
INSERT INTO fb_hashtags (hashid, hash_tag, hash_post_count, hash_created) VALUES (4, 'art', 2, '2023-03-01');
INSERT INTO fb_hashtags (hashid, hash_tag, hash_post_count, hash_created) VALUES (5, 'music', 2, '2023-04-01');
INSERT INTO fb_hashtags (hashid, hash_tag, hash_post_count, hash_created) VALUES (6, 'tech', 1, '2023-05-01');
INSERT INTO fb_hashtags (hashid, hash_tag, hash_post_count, hash_created) VALUES (7, 'photography', 1, '2023-06-01');
INSERT INTO fb_hashtags (hashid, hash_tag, hash_post_count, hash_created) VALUES (8, 'wellness', 1, '2023-07-01');

-- =============================================
-- fb_post_hashtags (15 rows)
-- =============================================
CREATE TABLE fb_post_hashtags (
    phashid INTEGER PRIMARY KEY,
    phash_post_id INTEGER NOT NULL,
    phash_tag_text TEXT NOT NULL,
    phash_created TEXT
);

INSERT INTO fb_post_hashtags (phashid, phash_post_id, phash_tag_text, phash_created) VALUES (1, 1, 'travel', '2024-01-15');
INSERT INTO fb_post_hashtags (phashid, phash_post_id, phash_tag_text, phash_created) VALUES (2, 1, 'photography', '2024-01-15');
INSERT INTO fb_post_hashtags (phashid, phash_post_id, phash_tag_text, phash_created) VALUES (3, 3, 'food', '2024-01-20');
INSERT INTO fb_post_hashtags (phashid, phash_post_id, phash_tag_text, phash_created) VALUES (4, 5, 'travel', '2024-02-05');
INSERT INTO fb_post_hashtags (phashid, phash_post_id, phash_tag_text, phash_created) VALUES (5, 6, 'travel', '2024-04-12');
INSERT INTO fb_post_hashtags (phashid, phash_post_id, phash_tag_text, phash_created) VALUES (6, 7, 'fitness', '2024-01-25');
INSERT INTO fb_post_hashtags (phashid, phash_post_id, phash_tag_text, phash_created) VALUES (7, 8, 'fitness', '2024-03-18');
INSERT INTO fb_post_hashtags (phashid, phash_post_id, phash_tag_text, phash_created) VALUES (8, 9, 'art', '2024-02-10');
INSERT INTO fb_post_hashtags (phashid, phash_post_id, phash_tag_text, phash_created) VALUES (9, 10, 'art', '2024-04-01');
INSERT INTO fb_post_hashtags (phashid, phash_post_id, phash_tag_text, phash_created) VALUES (10, 15, 'tech', '2024-02-28');
INSERT INTO fb_post_hashtags (phashid, phash_post_id, phash_tag_text, phash_created) VALUES (11, 17, 'wellness', '2024-03-01');
INSERT INTO fb_post_hashtags (phashid, phash_post_id, phash_tag_text, phash_created) VALUES (12, 17, 'fitness', '2024-03-01');
INSERT INTO fb_post_hashtags (phashid, phash_post_id, phash_tag_text, phash_created) VALUES (13, 19, 'music', '2024-03-05');
INSERT INTO fb_post_hashtags (phashid, phash_post_id, phash_tag_text, phash_created) VALUES (14, 20, 'music', '2024-04-15');
INSERT INTO fb_post_hashtags (phashid, phash_post_id, phash_tag_text, phash_created) VALUES (15, 5, 'food', '2024-02-05');
"""

TARGET_SQL = """
-- Instagram-style Unified Schema
-- Proper FKs, NOT NULL, UNIQUE, DEFAULT constraints

-- =============================================
-- accounts (10 rows)
-- =============================================
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    password_hash TEXT NOT NULL,
    account_status TEXT NOT NULL DEFAULT 'active',
    account_type TEXT NOT NULL DEFAULT 'personal',
    created_at TEXT NOT NULL,
    last_login_at TEXT,
    is_verified INTEGER NOT NULL DEFAULT 0
);

INSERT INTO accounts VALUES (1, 'alice_chen', 'alice@facebook.com', '555-0101', 'hashed_pw_alice01', 'active', 'personal', '2020-01-15', NULL, 0);
INSERT INTO accounts VALUES (2, 'bob_rivera', 'bob@facebook.com', '555-0102', 'hashed_pw_bob02', 'active', 'personal', '2020-03-10', NULL, 0);
INSERT INTO accounts VALUES (3, 'carol_zhang', 'carol@facebook.com', '555-0103', 'hashed_pw_carol03', 'active', 'personal', '2020-06-20', NULL, 0);
INSERT INTO accounts VALUES (4, 'dave_wilson', 'dave@facebook.com', '555-0104', 'hashed_pw_dave04', 'active', 'personal', '2020-09-05', NULL, 0);
INSERT INTO accounts VALUES (5, 'eve_thompson', 'eve@facebook.com', '555-0105', 'hashed_pw_eve05', 'active', 'personal', '2021-01-10', NULL, 0);
INSERT INTO accounts VALUES (6, 'frank_garcia', 'frank@facebook.com', '555-0106', 'hashed_pw_frank06', 'active', 'personal', '2021-04-18', NULL, 0);
INSERT INTO accounts VALUES (7, 'grace_kim', 'grace@facebook.com', '555-0107', 'hashed_pw_grace07', 'active', 'personal', '2021-07-22', NULL, 0);
INSERT INTO accounts VALUES (8, 'henry_patel', 'henry@facebook.com', '555-0108', 'hashed_pw_henry08', 'active', 'personal', '2021-10-30', NULL, 0);
INSERT INTO accounts VALUES (9, 'ivy_santos', 'ivy@facebook.com', '555-0109', 'hashed_pw_ivy09', 'active', 'personal', '2022-02-14', NULL, 0);
INSERT INTO accounts VALUES (10, 'jack_murphy', 'jack@facebook.com', '555-0110', 'hashed_pw_jack10', 'active', 'personal', '2022-05-01', NULL, 0);

-- =============================================
-- profiles (10 rows)
-- =============================================
CREATE TABLE profiles (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    display_name TEXT,
    bio TEXT,
    avatar_url TEXT,
    website TEXT,
    occupation TEXT,
    gender TEXT,
    date_of_birth TEXT,
    city TEXT,
    country TEXT,
    is_public INTEGER NOT NULL DEFAULT 1
);

INSERT INTO profiles VALUES (1, 1, 'Alice Chen', 'Tech enthusiast and photographer', '/avatars/alice.jpg', 'https://alicechen.dev', 'Software Engineer', 'female', '1990-03-15', 'San Francisco', 'US', 1);
INSERT INTO profiles VALUES (2, 2, 'Bob Rivera', 'Music lover and foodie', '/avatars/bob.jpg', NULL, 'Chef', 'male', '1985-07-22', 'Austin', 'US', 1);
INSERT INTO profiles VALUES (3, 3, 'Carol Zhang', 'Travel blogger exploring the world', '/avatars/carol.jpg', 'https://carolztravels.com', 'Travel Blogger', 'female', '1992-11-08', 'Seattle', 'US', 1);
INSERT INTO profiles VALUES (4, 4, 'Dave Wilson', 'Outdoor adventurer and fitness buff', '/avatars/dave.jpg', NULL, 'Personal Trainer', 'male', '1988-01-30', 'Denver', 'US', 0);
INSERT INTO profiles VALUES (5, 5, 'Eve Thompson', 'Digital artist and designer', '/avatars/eve.jpg', 'https://evedesigns.co', 'Graphic Designer', 'female', '1995-05-12', 'Miami', 'US', 1);
INSERT INTO profiles VALUES (6, 6, 'Frank Garcia', 'Startup founder and mentor', '/avatars/frank.jpg', 'https://frankgarcia.biz', 'Entrepreneur', 'male', '1983-09-25', 'Chicago', 'US', 1);
INSERT INTO profiles VALUES (7, 7, 'Grace Kim', 'Film critic and cinephile', '/avatars/grace.jpg', NULL, 'Film Critic', 'female', '1991-12-03', 'Los Angeles', 'US', 1);
INSERT INTO profiles VALUES (8, 8, 'Henry Patel', 'Data scientist by day, gamer by night', '/avatars/henry.jpg', 'https://henrypatel.io', 'Data Scientist', 'male', '1987-04-18', 'Boston', 'US', 0);
INSERT INTO profiles VALUES (9, 9, 'Ivy Santos', 'Yoga instructor and wellness coach', '/avatars/ivy.jpg', 'https://ivywellness.com', 'Yoga Instructor', 'female', '1994-08-07', 'Phoenix', 'US', 1);
INSERT INTO profiles VALUES (10, 10, 'Jack Murphy', 'Musician and songwriter', '/avatars/jack.jpg', 'https://jackmurphymusic.com', 'Musician', 'male', '1986-02-14', 'Nashville', 'US', 1);

-- =============================================
-- account_settings (10 rows)
-- =============================================
CREATE TABLE account_settings (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    default_privacy TEXT NOT NULL DEFAULT 'public',
    notification_email INTEGER NOT NULL DEFAULT 1,
    notification_push INTEGER NOT NULL DEFAULT 1,
    notification_sms INTEGER NOT NULL DEFAULT 0,
    language TEXT NOT NULL DEFAULT 'en',
    theme TEXT NOT NULL DEFAULT 'light',
    two_factor_enabled INTEGER NOT NULL DEFAULT 0
);

INSERT INTO account_settings VALUES (1, 1, 'public', 1, 1, 0, 'en', 'light', 0);
INSERT INTO account_settings VALUES (2, 2, 'public', 1, 1, 0, 'en', 'light', 0);
INSERT INTO account_settings VALUES (3, 3, 'public', 1, 1, 0, 'en', 'light', 0);
INSERT INTO account_settings VALUES (4, 4, 'friends', 1, 1, 0, 'en', 'light', 0);
INSERT INTO account_settings VALUES (5, 5, 'public', 1, 1, 0, 'en', 'light', 0);
INSERT INTO account_settings VALUES (6, 6, 'public', 1, 1, 0, 'en', 'light', 0);
INSERT INTO account_settings VALUES (7, 7, 'public', 1, 1, 0, 'en', 'light', 0);
INSERT INTO account_settings VALUES (8, 8, 'friends', 1, 1, 0, 'en', 'light', 0);
INSERT INTO account_settings VALUES (9, 9, 'public', 1, 1, 0, 'en', 'light', 0);
INSERT INTO account_settings VALUES (10, 10, 'public', 1, 1, 0, 'en', 'light', 0);

-- =============================================
-- follow_relationships (15 rows)
-- =============================================
CREATE TABLE follow_relationships (
    id INTEGER PRIMARY KEY,
    follower_id INTEGER NOT NULL REFERENCES accounts(id),
    following_id INTEGER NOT NULL REFERENCES accounts(id),
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL
);

INSERT INTO follow_relationships VALUES (1, 1, 2, 'active', '2020-04-01');
INSERT INTO follow_relationships VALUES (2, 1, 3, 'active', '2020-07-15');
INSERT INTO follow_relationships VALUES (3, 1, 4, 'active', '2020-10-20');
INSERT INTO follow_relationships VALUES (4, 2, 3, 'active', '2020-08-05');
INSERT INTO follow_relationships VALUES (5, 2, 5, 'active', '2021-02-14');
INSERT INTO follow_relationships VALUES (6, 3, 6, 'active', '2021-05-10');
INSERT INTO follow_relationships VALUES (7, 4, 7, 'active', '2021-08-22');
INSERT INTO follow_relationships VALUES (8, 5, 8, 'active', '2021-11-30');
INSERT INTO follow_relationships VALUES (9, 6, 9, 'active', '2022-03-15');
INSERT INTO follow_relationships VALUES (10, 7, 10, 'active', '2022-06-01');
INSERT INTO follow_relationships VALUES (11, 8, 1, 'active', '2022-01-10');
INSERT INTO follow_relationships VALUES (12, 9, 2, 'pending', '2023-04-20');
INSERT INTO follow_relationships VALUES (13, 10, 3, 'active', '2023-01-05');
INSERT INTO follow_relationships VALUES (14, 4, 6, 'active', '2022-09-12');
INSERT INTO follow_relationships VALUES (15, 5, 7, 'active', '2023-02-28');

-- =============================================
-- blocked_accounts (5 rows)
-- =============================================
CREATE TABLE blocked_accounts (
    id INTEGER PRIMARY KEY,
    blocker_id INTEGER NOT NULL REFERENCES accounts(id),
    blocked_id INTEGER NOT NULL REFERENCES accounts(id),
    reason TEXT,
    created_at TEXT NOT NULL
);

INSERT INTO blocked_accounts VALUES (1, 1, 10, 'Spam messages', '2023-06-15');
INSERT INTO blocked_accounts VALUES (2, 2, 6, 'Harassment', '2023-09-20');
INSERT INTO blocked_accounts VALUES (3, 3, 8, 'Unwanted contact', '2024-01-05');
INSERT INTO blocked_accounts VALUES (4, 4, 9, 'Inappropriate content', '2024-02-10');
INSERT INTO blocked_accounts VALUES (5, 5, 2, 'Privacy concerns', '2024-03-01');

-- =============================================
-- account_verifications (10 rows)
-- =============================================
CREATE TABLE account_verifications (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    verification_type TEXT NOT NULL DEFAULT 'email',
    verified_at TEXT,
    document_url TEXT
);

INSERT INTO account_verifications VALUES (1, 1, 'email', '2020-01-15', NULL);
INSERT INTO account_verifications VALUES (2, 2, 'email', '2020-03-10', NULL);
INSERT INTO account_verifications VALUES (3, 3, 'email', '2020-06-20', NULL);
INSERT INTO account_verifications VALUES (4, 4, 'email', '2020-09-05', NULL);
INSERT INTO account_verifications VALUES (5, 5, 'email', '2021-01-10', NULL);
INSERT INTO account_verifications VALUES (6, 6, 'email', '2021-04-18', NULL);
INSERT INTO account_verifications VALUES (7, 7, 'email', '2021-07-22', NULL);
INSERT INTO account_verifications VALUES (8, 8, 'email', '2021-10-30', NULL);
INSERT INTO account_verifications VALUES (9, 9, 'email', '2022-02-14', NULL);
INSERT INTO account_verifications VALUES (10, 10, 'email', '2022-05-01', NULL);

-- =============================================
-- media_posts (20 rows)
-- =============================================
CREATE TABLE media_posts (
    id INTEGER PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES accounts(id),
    caption TEXT,
    media_type TEXT NOT NULL DEFAULT 'photo',
    media_url TEXT,
    thumbnail_url TEXT,
    privacy TEXT NOT NULL DEFAULT 'public',
    location TEXT,
    is_archived INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT
);

INSERT INTO media_posts VALUES (1, 1, 'Just landed in Tokyo! Amazing city vibes', 'photo', '/media/posts/alice_tokyo.jpg', NULL, 'public', NULL, 0, '2024-01-15', '2024-01-15');
INSERT INTO media_posts VALUES (2, 1, 'New coding project launched today @bob_rivera check it out', 'text', NULL, NULL, 'public', NULL, 0, '2024-02-20', '2024-02-20');
INSERT INTO media_posts VALUES (3, 2, 'Made the perfect sourdough bread today', 'photo', '/media/posts/bob_bread.jpg', NULL, 'public', NULL, 0, '2024-01-20', '2024-01-20');
INSERT INTO media_posts VALUES (4, 2, 'Concert night with @eve_thompson', 'photo', '/media/posts/bob_concert.jpg', NULL, 'friends', NULL, 0, '2024-03-10', '2024-03-10');
INSERT INTO media_posts VALUES (5, 3, 'Exploring the streets of Barcelona', 'video', '/media/posts/carol_barcelona.mp4', NULL, 'public', NULL, 0, '2024-02-05', '2024-02-05');
INSERT INTO media_posts VALUES (6, 3, 'Best hiking trail I have ever been on', 'photo', '/media/posts/carol_hiking.jpg', NULL, 'public', NULL, 0, '2024-04-12', '2024-04-12');
INSERT INTO media_posts VALUES (7, 4, 'Morning workout routine - 5am club', 'video', '/media/posts/dave_workout.mp4', NULL, 'public', NULL, 0, '2024-01-25', '2024-01-25');
INSERT INTO media_posts VALUES (8, 4, 'Mountain biking in Colorado', 'photo', '/media/posts/dave_biking.jpg', NULL, 'public', NULL, 0, '2024-03-18', '2024-03-18');
INSERT INTO media_posts VALUES (9, 5, 'New digital art piece - Neon Dreams', 'photo', '/media/posts/eve_neon.jpg', NULL, 'public', NULL, 0, '2024-02-10', '2024-02-10');
INSERT INTO media_posts VALUES (10, 5, 'Design tips for beginners thread', 'text', NULL, NULL, 'public', NULL, 0, '2024-04-01', '2024-04-02');
INSERT INTO media_posts VALUES (11, 6, 'Startup lessons learned this year', 'text', NULL, NULL, 'public', NULL, 0, '2024-01-30', '2024-01-30');
INSERT INTO media_posts VALUES (12, 6, 'Team building event at the office', 'photo', '/media/posts/frank_team.jpg', NULL, 'friends', NULL, 0, '2024-03-25', '2024-03-25');
INSERT INTO media_posts VALUES (13, 7, 'Just watched the new Nolan film - mind blown', 'text', NULL, NULL, 'public', NULL, 0, '2024-02-15', '2024-02-15');
INSERT INTO media_posts VALUES (14, 7, 'Oscar predictions for this year', 'link', 'https://gracereviewsblog.com/oscars', NULL, 'public', NULL, 0, '2024-04-05', '2024-04-05');
INSERT INTO media_posts VALUES (15, 8, 'Data visualization of climate trends', 'photo', '/media/posts/henry_dataviz.jpg', NULL, 'public', NULL, 0, '2024-02-28', '2024-02-28');
INSERT INTO media_posts VALUES (16, 8, 'Gaming session highlights', 'video', '/media/posts/henry_gaming.mp4', NULL, 'friends', NULL, 0, '2024-03-30', '2024-03-30');
INSERT INTO media_posts VALUES (17, 9, 'Sunrise yoga on the beach', 'photo', '/media/posts/ivy_yoga.jpg', NULL, 'public', NULL, 0, '2024-03-01', '2024-03-01');
INSERT INTO media_posts VALUES (18, 9, 'Wellness tips for a balanced life', 'text', NULL, NULL, 'public', NULL, 0, '2024-04-10', '2024-04-10');
INSERT INTO media_posts VALUES (19, 10, 'New song out now - listen on all platforms', 'link', 'https://music.example.com/jack_newsong', NULL, 'public', NULL, 0, '2024-03-05', '2024-03-05');
INSERT INTO media_posts VALUES (20, 10, 'Behind the scenes of the recording studio', 'video', '/media/posts/jack_studio.mp4', NULL, 'public', NULL, 0, '2024-04-15', '2024-04-15');

-- =============================================
-- post_comments (25 rows)
-- =============================================
CREATE TABLE post_comments (
    id INTEGER PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES media_posts(id),
    author_id INTEGER NOT NULL REFERENCES accounts(id),
    parent_comment_id INTEGER REFERENCES post_comments(id),
    comment_text TEXT NOT NULL,
    is_edited INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

INSERT INTO post_comments VALUES (1, 1, 2, NULL, 'Looks amazing! Enjoy your trip!', 0, '2024-01-15');
INSERT INTO post_comments VALUES (2, 1, 3, NULL, 'I love Tokyo! Try the ramen at Ichiran', 0, '2024-01-15');
INSERT INTO post_comments VALUES (3, 1, 1, 2, 'Thanks Carol! Will definitely check it out', 0, '2024-01-16');
INSERT INTO post_comments VALUES (4, 3, 1, NULL, 'That bread looks incredible!', 0, '2024-01-20');
INSERT INTO post_comments VALUES (5, 3, 5, NULL, 'Recipe please!', 0, '2024-01-21');
INSERT INTO post_comments VALUES (6, 3, 2, 5, 'Thanks! Will share the recipe soon', 0, '2024-01-21');
INSERT INTO post_comments VALUES (7, 5, 1, NULL, 'Barcelona is on my bucket list!', 0, '2024-02-05');
INSERT INTO post_comments VALUES (8, 5, 4, NULL, 'Beautiful footage Carol!', 0, '2024-02-06');
INSERT INTO post_comments VALUES (9, 7, 6, NULL, 'That is dedication! How do you wake up so early?', 0, '2024-01-25');
INSERT INTO post_comments VALUES (10, 7, 4, 9, 'Discipline and a good alarm clock!', 0, '2024-01-26');
INSERT INTO post_comments VALUES (11, 9, 7, NULL, 'This is stunning! What software do you use?', 0, '2024-02-10');
INSERT INTO post_comments VALUES (12, 9, 5, 11, 'I use Procreate and Photoshop combo', 0, '2024-02-11');
INSERT INTO post_comments VALUES (13, 11, 8, NULL, 'Great insights! Very relatable', 0, '2024-01-30');
INSERT INTO post_comments VALUES (14, 13, 10, NULL, 'Nolan never disappoints', 0, '2024-02-15');
INSERT INTO post_comments VALUES (15, 13, 1, NULL, 'Need to watch this ASAP', 0, '2024-02-16');
INSERT INTO post_comments VALUES (16, 15, 3, NULL, 'Important work Henry, thanks for sharing', 0, '2024-02-28');
INSERT INTO post_comments VALUES (17, 15, 6, NULL, 'Eye opening visualization', 0, '2024-03-01');
INSERT INTO post_comments VALUES (18, 17, 1, NULL, 'This is so peaceful!', 0, '2024-03-01');
INSERT INTO post_comments VALUES (19, 17, 5, NULL, 'I need to try beach yoga', 0, '2024-03-02');
INSERT INTO post_comments VALUES (20, 19, 2, NULL, 'Fire track! On repeat all day', 0, '2024-03-05');
INSERT INTO post_comments VALUES (21, 19, 7, NULL, 'Your best work yet Jack!', 0, '2024-03-06');
INSERT INTO post_comments VALUES (22, 19, 10, 21, 'Thanks Grace! Means a lot', 0, '2024-03-06');
INSERT INTO post_comments VALUES (23, 10, 9, NULL, 'Super helpful thread Eve!', 0, '2024-04-01');
INSERT INTO post_comments VALUES (24, 8, 8, NULL, 'Colorado has the best trails', 0, '2024-03-18');
INSERT INTO post_comments VALUES (25, 20, 9, NULL, 'Love the behind the scenes content!', 0, '2024-04-15');

-- =============================================
-- post_likes (18 rows)
-- =============================================
CREATE TABLE post_likes (
    id INTEGER PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES media_posts(id),
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    created_at TEXT NOT NULL
);

INSERT INTO post_likes VALUES (1, 1, 2, '2024-01-15');
INSERT INTO post_likes VALUES (2, 1, 3, '2024-01-15');
INSERT INTO post_likes VALUES (3, 1, 4, '2024-01-16');
INSERT INTO post_likes VALUES (4, 3, 1, '2024-01-20');
INSERT INTO post_likes VALUES (5, 3, 5, '2024-01-21');
INSERT INTO post_likes VALUES (6, 5, 3, '2024-02-05');
INSERT INTO post_likes VALUES (7, 5, 1, '2024-02-06');
INSERT INTO post_likes VALUES (8, 7, 6, '2024-01-25');
INSERT INTO post_likes VALUES (9, 9, 7, '2024-02-10');
INSERT INTO post_likes VALUES (10, 9, 8, '2024-02-11');
INSERT INTO post_likes VALUES (11, 11, 10, '2024-01-30');
INSERT INTO post_likes VALUES (12, 13, 1, '2024-02-15');
INSERT INTO post_likes VALUES (13, 15, 3, '2024-02-28');
INSERT INTO post_likes VALUES (14, 17, 2, '2024-03-01');
INSERT INTO post_likes VALUES (15, 17, 5, '2024-03-02');
INSERT INTO post_likes VALUES (16, 19, 7, '2024-03-05');
INSERT INTO post_likes VALUES (17, 19, 8, '2024-03-06');
INSERT INTO post_likes VALUES (18, 20, 9, '2024-04-15');

-- =============================================
-- comment_likes (12 rows)
-- =============================================
CREATE TABLE comment_likes (
    id INTEGER PRIMARY KEY,
    comment_id INTEGER NOT NULL REFERENCES post_comments(id),
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    created_at TEXT NOT NULL
);

INSERT INTO comment_likes VALUES (1, 1, 2, '2024-01-15');
INSERT INTO comment_likes VALUES (2, 2, 1, '2024-01-16');
INSERT INTO comment_likes VALUES (3, 4, 3, '2024-01-21');
INSERT INTO comment_likes VALUES (4, 7, 4, '2024-02-06');
INSERT INTO comment_likes VALUES (5, 9, 6, '2024-01-26');
INSERT INTO comment_likes VALUES (6, 11, 7, '2024-02-11');
INSERT INTO comment_likes VALUES (7, 13, 8, '2024-01-31');
INSERT INTO comment_likes VALUES (8, 14, 10, '2024-02-16');
INSERT INTO comment_likes VALUES (9, 18, 1, '2024-03-02');
INSERT INTO comment_likes VALUES (10, 20, 5, '2024-03-06');
INSERT INTO comment_likes VALUES (11, 21, 9, '2024-03-07');
INSERT INTO comment_likes VALUES (12, 25, 6, '2024-04-16');

-- =============================================
-- saved_posts (10 rows)
-- =============================================
CREATE TABLE saved_posts (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    post_id INTEGER NOT NULL REFERENCES media_posts(id),
    collection_name TEXT NOT NULL DEFAULT 'All Posts',
    saved_at TEXT NOT NULL
);

INSERT INTO saved_posts VALUES (1, 1, 5, 'All Posts', '2024-02-06');
INSERT INTO saved_posts VALUES (2, 1, 9, 'All Posts', '2024-02-11');
INSERT INTO saved_posts VALUES (3, 2, 1, 'All Posts', '2024-01-16');
INSERT INTO saved_posts VALUES (4, 3, 17, 'All Posts', '2024-03-02');
INSERT INTO saved_posts VALUES (5, 4, 7, 'All Posts', '2024-01-26');
INSERT INTO saved_posts VALUES (6, 5, 19, 'All Posts', '2024-03-06');
INSERT INTO saved_posts VALUES (7, 7, 15, 'All Posts', '2024-02-28');
INSERT INTO saved_posts VALUES (8, 8, 9, 'All Posts', '2024-02-12');
INSERT INTO saved_posts VALUES (9, 9, 3, 'All Posts', '2024-01-22');
INSERT INTO saved_posts VALUES (10, 10, 13, 'All Posts', '2024-02-16');

-- =============================================
-- media_albums (8 rows)
-- =============================================
CREATE TABLE media_albums (
    id INTEGER PRIMARY KEY,
    owner_id INTEGER NOT NULL REFERENCES accounts(id),
    album_name TEXT NOT NULL,
    description TEXT,
    privacy TEXT NOT NULL DEFAULT 'public',
    cover_url TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT
);

INSERT INTO media_albums VALUES (1, 1, 'Travel 2024', 'Photos from my travels in 2024', 'public', '/photos/alice_tokyo1.jpg', '2024-01-10', NULL);
INSERT INTO media_albums VALUES (2, 2, 'Food Adventures', 'My culinary creations', 'public', '/photos/bob_bread1.jpg', '2024-01-15', NULL);
INSERT INTO media_albums VALUES (3, 3, 'Wanderlust', 'Places I have explored', 'public', '/photos/carol_barca1.jpg', '2024-01-20', NULL);
INSERT INTO media_albums VALUES (4, 4, 'Fitness Journey', 'Workout and outdoor photos', 'friends', '/photos/dave_gym1.jpg', '2024-01-22', NULL);
INSERT INTO media_albums VALUES (5, 5, 'My Art', 'Digital art portfolio', 'public', '/photos/eve_neon1.jpg', '2024-02-01', NULL);
INSERT INTO media_albums VALUES (6, 7, 'Movie Nights', 'Cinema and film events', 'public', '/photos/grace_cinema1.jpg', '2024-02-10', NULL);
INSERT INTO media_albums VALUES (7, 8, 'Data & Code', 'Visualizations and projects', 'private', '/photos/henry_dataviz1.jpg', '2024-02-20', NULL);
INSERT INTO media_albums VALUES (8, 10, 'Music Studio', 'Studio life and instruments', 'public', '/photos/jack_guitar1.jpg', '2024-03-01', NULL);

-- =============================================
-- album_media (8 rows)
-- =============================================
CREATE TABLE album_media (
    id INTEGER PRIMARY KEY,
    album_id INTEGER NOT NULL REFERENCES media_albums(id),
    post_id INTEGER NOT NULL REFERENCES media_posts(id),
    sort_order INTEGER NOT NULL DEFAULT 0,
    added_at TEXT NOT NULL
);

INSERT INTO album_media VALUES (1, 1, 1, 0, '2024-01-15');
INSERT INTO album_media VALUES (2, 2, 3, 0, '2024-01-20');
INSERT INTO album_media VALUES (3, 3, 5, 0, '2024-02-05');
INSERT INTO album_media VALUES (4, 3, 6, 1, '2024-04-12');
INSERT INTO album_media VALUES (5, 4, 7, 0, '2024-01-25');
INSERT INTO album_media VALUES (6, 4, 8, 1, '2024-03-18');
INSERT INTO album_media VALUES (7, 5, 9, 0, '2024-02-10');
INSERT INTO album_media VALUES (8, 8, 20, 0, '2024-04-15');

-- =============================================
-- hashtags (8 rows)
-- =============================================
CREATE TABLE hashtags (
    id INTEGER PRIMARY KEY,
    tag_name TEXT NOT NULL UNIQUE,
    usage_count INTEGER NOT NULL DEFAULT 0,
    is_trending INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

INSERT INTO hashtags VALUES (1, 'travel', 4, 1, '2023-01-01');
INSERT INTO hashtags VALUES (2, 'food', 2, 0, '2023-01-01');
INSERT INTO hashtags VALUES (3, 'fitness', 3, 1, '2023-02-01');
INSERT INTO hashtags VALUES (4, 'art', 2, 0, '2023-03-01');
INSERT INTO hashtags VALUES (5, 'music', 2, 0, '2023-04-01');
INSERT INTO hashtags VALUES (6, 'tech', 1, 0, '2023-05-01');
INSERT INTO hashtags VALUES (7, 'photography', 1, 0, '2023-06-01');
INSERT INTO hashtags VALUES (8, 'wellness', 1, 0, '2023-07-01');

-- =============================================
-- post_hashtags (15 rows)
-- =============================================
CREATE TABLE post_hashtags (
    id INTEGER PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES media_posts(id),
    hashtag_id INTEGER NOT NULL REFERENCES hashtags(id),
    created_at TEXT NOT NULL
);

INSERT INTO post_hashtags VALUES (1, 1, 1, '2024-01-15');
INSERT INTO post_hashtags VALUES (2, 1, 7, '2024-01-15');
INSERT INTO post_hashtags VALUES (3, 3, 2, '2024-01-20');
INSERT INTO post_hashtags VALUES (4, 5, 1, '2024-02-05');
INSERT INTO post_hashtags VALUES (5, 6, 1, '2024-04-12');
INSERT INTO post_hashtags VALUES (6, 7, 3, '2024-01-25');
INSERT INTO post_hashtags VALUES (7, 8, 3, '2024-03-18');
INSERT INTO post_hashtags VALUES (8, 9, 4, '2024-02-10');
INSERT INTO post_hashtags VALUES (9, 10, 4, '2024-04-01');
INSERT INTO post_hashtags VALUES (10, 15, 6, '2024-02-28');
INSERT INTO post_hashtags VALUES (11, 17, 8, '2024-03-01');
INSERT INTO post_hashtags VALUES (12, 17, 3, '2024-03-01');
INSERT INTO post_hashtags VALUES (13, 19, 5, '2024-03-05');
INSERT INTO post_hashtags VALUES (14, 20, 5, '2024-04-15');
INSERT INTO post_hashtags VALUES (15, 5, 2, '2024-02-05');

-- =============================================
-- post_mentions (6 rows)
-- =============================================
CREATE TABLE post_mentions (
    id INTEGER PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES media_posts(id),
    mentioned_account_id INTEGER NOT NULL REFERENCES accounts(id),
    created_at TEXT NOT NULL
);

INSERT INTO post_mentions VALUES (1, 2, 2, '2024-02-20');
INSERT INTO post_mentions VALUES (2, 4, 5, '2024-03-10');
INSERT INTO post_mentions VALUES (3, 2, 1, '2024-02-20');
INSERT INTO post_mentions VALUES (4, 4, 2, '2024-03-10');
INSERT INTO post_mentions VALUES (5, 10, 5, '2024-04-01');
INSERT INTO post_mentions VALUES (6, 19, 10, '2024-03-05');

-- =============================================
-- post_shares (5 rows)
-- =============================================
CREATE TABLE post_shares (
    id INTEGER PRIMARY KEY,
    original_post_id INTEGER NOT NULL REFERENCES media_posts(id),
    shared_by_id INTEGER NOT NULL REFERENCES accounts(id),
    share_type TEXT NOT NULL DEFAULT 'repost',
    shared_at TEXT NOT NULL
);

INSERT INTO post_shares VALUES (1, 1, 3, 'repost', '2024-01-16');
INSERT INTO post_shares VALUES (2, 5, 1, 'repost', '2024-02-06');
INSERT INTO post_shares VALUES (3, 9, 7, 'repost', '2024-02-11');
INSERT INTO post_shares VALUES (4, 17, 1, 'repost', '2024-03-02');
INSERT INTO post_shares VALUES (5, 19, 2, 'repost', '2024-03-06');

-- =============================================
-- stories (5 rows)
-- =============================================
CREATE TABLE stories (
    id INTEGER PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES accounts(id),
    media_url TEXT NOT NULL,
    media_type TEXT NOT NULL DEFAULT 'photo',
    caption TEXT,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    is_highlight INTEGER NOT NULL DEFAULT 0
);

INSERT INTO stories VALUES (1, 1, '/stories/alice_morning.jpg', 'photo', 'Good morning from SF!', '2024-04-10', '2024-04-11', 0);
INSERT INTO stories VALUES (2, 3, '/stories/carol_sunset.jpg', 'photo', 'Sunset views', '2024-04-11', '2024-04-12', 1);
INSERT INTO stories VALUES (3, 5, '/stories/eve_sketch.jpg', 'photo', 'Quick sketch session', '2024-04-12', '2024-04-13', 0);
INSERT INTO stories VALUES (4, 9, '/stories/ivy_meditation.jpg', 'photo', 'Meditation time', '2024-04-13', '2024-04-14', 1);
INSERT INTO stories VALUES (5, 10, '/stories/jack_rehearsal.jpg', 'photo', 'Rehearsal vibes', '2024-04-14', '2024-04-15', 0);

-- =============================================
-- story_views (10 rows)
-- =============================================
CREATE TABLE story_views (
    id INTEGER PRIMARY KEY,
    story_id INTEGER NOT NULL REFERENCES stories(id),
    viewer_id INTEGER NOT NULL REFERENCES accounts(id),
    viewed_at TEXT NOT NULL
);

INSERT INTO story_views VALUES (1, 1, 2, '2024-04-10');
INSERT INTO story_views VALUES (2, 1, 3, '2024-04-10');
INSERT INTO story_views VALUES (3, 2, 1, '2024-04-11');
INSERT INTO story_views VALUES (4, 2, 4, '2024-04-11');
INSERT INTO story_views VALUES (5, 3, 7, '2024-04-12');
INSERT INTO story_views VALUES (6, 3, 1, '2024-04-12');
INSERT INTO story_views VALUES (7, 4, 1, '2024-04-13');
INSERT INTO story_views VALUES (8, 4, 5, '2024-04-13');
INSERT INTO story_views VALUES (9, 5, 7, '2024-04-14');
INSERT INTO story_views VALUES (10, 5, 2, '2024-04-14');

-- =============================================
-- story_highlights (4 rows)
-- =============================================
CREATE TABLE story_highlights (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    highlight_name TEXT NOT NULL,
    cover_url TEXT,
    created_at TEXT NOT NULL
);

INSERT INTO story_highlights VALUES (1, 1, 'Travel', '/highlights/travel_cover.jpg', '2024-04-10');
INSERT INTO story_highlights VALUES (2, 3, 'Adventures', '/highlights/adventures_cover.jpg', '2024-04-11');
INSERT INTO story_highlights VALUES (3, 5, 'Art Process', '/highlights/art_cover.jpg', '2024-04-12');
INSERT INTO story_highlights VALUES (4, 9, 'Wellness', '/highlights/wellness_cover.jpg', '2024-04-13');

-- =============================================
-- communities (6 rows)
-- =============================================
CREATE TABLE communities (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT NOT NULL,
    description TEXT,
    creator_id INTEGER NOT NULL REFERENCES accounts(id),
    privacy TEXT NOT NULL DEFAULT 'public',
    cover_url TEXT,
    member_count INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
);

INSERT INTO communities VALUES (1, 'Tech Enthusiasts', 'tech-enthusiasts', 'A community for technology lovers', 1, 'public', NULL, 5, '2021-03-01', 1);
INSERT INTO communities VALUES (2, 'Foodies United', 'foodies-united', 'Share your favorite recipes and restaurants', 2, 'public', NULL, 4, '2021-06-15', 1);
INSERT INTO communities VALUES (3, 'Travel Bugs', 'travel-bugs', 'For passionate travelers sharing experiences', 3, 'public', NULL, 3, '2021-09-10', 1);
INSERT INTO communities VALUES (4, 'Fitness Warriors', 'fitness-warriors', 'Workout tips and motivation', 4, 'private', NULL, 3, '2022-01-05', 1);
INSERT INTO communities VALUES (5, 'Creative Arts', 'creative-arts', 'Digital art, design, and photography', 5, 'public', NULL, 2, '2022-04-20', 1);
INSERT INTO communities VALUES (6, 'Music Makers', 'music-makers', 'Musicians and songwriters connect here', 10, 'public', NULL, 1, '2022-08-01', 1);

-- =============================================
-- community_members (18 rows)
-- =============================================
CREATE TABLE community_members (
    id INTEGER PRIMARY KEY,
    community_id INTEGER NOT NULL REFERENCES communities(id),
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    role TEXT NOT NULL DEFAULT 'member',
    joined_at TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
);

INSERT INTO community_members VALUES (1, 1, 1, 'admin', '2021-03-01', 1);
INSERT INTO community_members VALUES (2, 1, 8, 'moderator', '2021-03-15', 1);
INSERT INTO community_members VALUES (3, 1, 6, 'member', '2021-04-01', 1);
INSERT INTO community_members VALUES (4, 1, 2, 'member', '2021-05-10', 1);
INSERT INTO community_members VALUES (5, 1, 7, 'member', '2021-06-20', 1);
INSERT INTO community_members VALUES (6, 2, 2, 'admin', '2021-06-15', 1);
INSERT INTO community_members VALUES (7, 2, 1, 'member', '2021-07-01', 1);
INSERT INTO community_members VALUES (8, 2, 3, 'member', '2021-07-20', 1);
INSERT INTO community_members VALUES (9, 2, 9, 'member', '2022-01-10', 1);
INSERT INTO community_members VALUES (10, 3, 3, 'admin', '2021-09-10', 1);
INSERT INTO community_members VALUES (11, 3, 1, 'member', '2021-10-01', 1);
INSERT INTO community_members VALUES (12, 3, 4, 'member', '2022-02-15', 1);
INSERT INTO community_members VALUES (13, 4, 4, 'admin', '2022-01-05', 1);
INSERT INTO community_members VALUES (14, 4, 6, 'member', '2022-02-01', 1);
INSERT INTO community_members VALUES (15, 4, 9, 'member', '2022-03-15', 1);
INSERT INTO community_members VALUES (16, 5, 5, 'admin', '2022-04-20', 1);
INSERT INTO community_members VALUES (17, 5, 7, 'member', '2022-05-10', 1);
INSERT INTO community_members VALUES (18, 6, 10, 'admin', '2022-08-01', 1);

-- =============================================
-- community_posts (12 rows)
-- =============================================
CREATE TABLE community_posts (
    id INTEGER PRIMARY KEY,
    community_id INTEGER NOT NULL REFERENCES communities(id),
    author_id INTEGER NOT NULL REFERENCES accounts(id),
    content TEXT NOT NULL,
    media_url TEXT,
    created_at TEXT NOT NULL
);

INSERT INTO community_posts VALUES (1, 1, 1, 'Check out this new AI framework!', 'https://example.com/ai-framework', '2024-01-10');
INSERT INTO community_posts VALUES (2, 1, 8, 'Python 3.13 release notes discussion', NULL, '2024-02-01');
INSERT INTO community_posts VALUES (3, 1, 6, 'Best practices for microservices architecture', NULL, '2024-03-05');
INSERT INTO community_posts VALUES (4, 2, 2, 'My secret pasta sauce recipe', '/media/group/bob_sauce.jpg', '2024-01-20');
INSERT INTO community_posts VALUES (5, 2, 1, 'Best sushi in San Francisco', NULL, '2024-02-15');
INSERT INTO community_posts VALUES (6, 3, 3, 'Top 10 hidden gems in Southeast Asia', '/media/group/carol_asia.jpg', '2024-02-20');
INSERT INTO community_posts VALUES (7, 3, 1, 'Packing tips for long trips', NULL, '2024-03-10');
INSERT INTO community_posts VALUES (8, 4, 4, 'Weekly challenge: 100 push-ups daily', NULL, '2024-01-15');
INSERT INTO community_posts VALUES (9, 4, 6, 'Best protein shake recipes', '/media/group/frank_shake.jpg', '2024-02-10');
INSERT INTO community_posts VALUES (10, 5, 5, 'Free design resources for 2024', '/media/group/eve_resources.jpg', '2024-03-01');
INSERT INTO community_posts VALUES (11, 5, 7, 'Cinematography techniques for beginners', NULL, '2024-03-20');
INSERT INTO community_posts VALUES (12, 6, 10, 'Looking for collaborators on new album', NULL, '2024-04-01');

-- =============================================
-- community_rules (6 rows)
-- =============================================
CREATE TABLE community_rules (
    id INTEGER PRIMARY KEY,
    community_id INTEGER NOT NULL REFERENCES communities(id),
    rule_text TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

INSERT INTO community_rules VALUES (1, 1, 'Be respectful and constructive in discussions', 0, '2021-03-01');
INSERT INTO community_rules VALUES (2, 2, 'Only share original recipes or credit the source', 0, '2021-06-15');
INSERT INTO community_rules VALUES (3, 3, 'Include location details in travel posts', 0, '2021-09-10');
INSERT INTO community_rules VALUES (4, 4, 'No promoting unsafe workout practices', 0, '2022-01-05');
INSERT INTO community_rules VALUES (5, 5, 'Credit original artists when sharing work', 0, '2022-04-20');
INSERT INTO community_rules VALUES (6, 6, 'No self-promotion without contributing to discussions', 0, '2022-08-01');

-- =============================================
-- creator_accounts (5 rows)
-- =============================================
CREATE TABLE creator_accounts (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    page_name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    website TEXT,
    contact_email TEXT,
    is_verified INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

INSERT INTO creator_accounts VALUES (1, 1, 'Alice Tech Blog', 'Technology', 'Tech tutorials and coding tips', 'https://alicechen.dev', 'alice@facebook.com', 0, '2021-06-01');
INSERT INTO creator_accounts VALUES (2, 2, 'Bob Kitchen', 'Food & Drink', 'Recipes and cooking adventures', 'https://bobkitchen.com', 'bob@facebook.com', 0, '2021-09-15');
INSERT INTO creator_accounts VALUES (3, 3, 'Carol Travels', 'Travel', 'Travel guides and destination reviews', 'https://carolztravels.com', 'carol@facebook.com', 0, '2022-01-10');
INSERT INTO creator_accounts VALUES (4, 5, 'Eve Design Studio', 'Art & Design', 'Digital art showcase and tutorials', 'https://evedesigns.co', 'eve@facebook.com', 0, '2022-05-20');
INSERT INTO creator_accounts VALUES (5, 10, 'Jack Music', 'Music', 'Original music and live sessions', 'https://jackmurphymusic.com', 'jack@facebook.com', 0, '2022-09-01');

-- =============================================
-- creator_followers (12 rows)
-- =============================================
CREATE TABLE creator_followers (
    id INTEGER PRIMARY KEY,
    creator_account_id INTEGER NOT NULL REFERENCES creator_accounts(id),
    follower_id INTEGER NOT NULL REFERENCES accounts(id),
    followed_at TEXT NOT NULL
);

INSERT INTO creator_followers VALUES (1, 1, 2, '2021-07-01');
INSERT INTO creator_followers VALUES (2, 1, 8, '2021-11-15');
INSERT INTO creator_followers VALUES (3, 1, 6, '2022-03-01');
INSERT INTO creator_followers VALUES (4, 2, 1, '2021-10-01');
INSERT INTO creator_followers VALUES (5, 2, 3, '2022-02-14');
INSERT INTO creator_followers VALUES (6, 3, 1, '2022-02-01');
INSERT INTO creator_followers VALUES (7, 3, 4, '2022-04-10');
INSERT INTO creator_followers VALUES (8, 3, 9, '2022-06-20');
INSERT INTO creator_followers VALUES (9, 4, 7, '2022-06-15');
INSERT INTO creator_followers VALUES (10, 4, 1, '2022-08-01');
INSERT INTO creator_followers VALUES (11, 5, 2, '2022-10-01');
INSERT INTO creator_followers VALUES (12, 5, 7, '2023-01-15');

-- =============================================
-- creator_insights (5 rows) - COMPUTED
-- =============================================
CREATE TABLE creator_insights (
    id INTEGER PRIMARY KEY,
    creator_account_id INTEGER NOT NULL REFERENCES creator_accounts(id),
    total_followers INTEGER NOT NULL DEFAULT 0,
    total_posts INTEGER NOT NULL DEFAULT 0,
    avg_engagement_rate REAL
);

INSERT INTO creator_insights VALUES (1, 1, 3, 2, 5.5);
INSERT INTO creator_insights VALUES (2, 2, 2, 2, 10.5);
INSERT INTO creator_insights VALUES (3, 3, 3, 2, 15.0);
INSERT INTO creator_insights VALUES (4, 4, 2, 2, 20.0);
INSERT INTO creator_insights VALUES (5, 5, 2, 2, 19.0);

-- =============================================
-- dm_threads (8 rows)
-- =============================================
CREATE TABLE dm_threads (
    id INTEGER PRIMARY KEY,
    created_at TEXT NOT NULL,
    updated_at TEXT,
    is_group_chat INTEGER NOT NULL DEFAULT 0
);

INSERT INTO dm_threads VALUES (1, '2021-01-20', '2024-04-10', 0);
INSERT INTO dm_threads VALUES (2, '2021-03-15', '2024-03-25', 0);
INSERT INTO dm_threads VALUES (3, '2021-06-10', '2024-04-05', 0);
INSERT INTO dm_threads VALUES (4, '2022-01-05', '2024-03-15', 0);
INSERT INTO dm_threads VALUES (5, '2022-04-20', '2024-02-28', 0);
INSERT INTO dm_threads VALUES (6, '2022-07-15', '2024-04-12', 0);
INSERT INTO dm_threads VALUES (7, '2023-01-10', '2024-03-20', 0);
INSERT INTO dm_threads VALUES (8, '2023-05-01', '2024-04-08', 0);

-- =============================================
-- dm_participants (16 rows)
-- =============================================
CREATE TABLE dm_participants (
    id INTEGER PRIMARY KEY,
    thread_id INTEGER NOT NULL REFERENCES dm_threads(id),
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    joined_at TEXT NOT NULL,
    is_muted INTEGER NOT NULL DEFAULT 0
);

INSERT INTO dm_participants VALUES (1, 1, 1, '2021-01-20', 0);
INSERT INTO dm_participants VALUES (2, 1, 2, '2021-01-20', 0);
INSERT INTO dm_participants VALUES (3, 2, 1, '2021-03-15', 0);
INSERT INTO dm_participants VALUES (4, 2, 3, '2021-03-15', 0);
INSERT INTO dm_participants VALUES (5, 3, 2, '2021-06-10', 0);
INSERT INTO dm_participants VALUES (6, 3, 5, '2021-06-10', 0);
INSERT INTO dm_participants VALUES (7, 4, 3, '2022-01-05', 0);
INSERT INTO dm_participants VALUES (8, 4, 4, '2022-01-05', 0);
INSERT INTO dm_participants VALUES (9, 5, 4, '2022-04-20', 0);
INSERT INTO dm_participants VALUES (10, 5, 6, '2022-04-20', 0);
INSERT INTO dm_participants VALUES (11, 6, 5, '2022-07-15', 0);
INSERT INTO dm_participants VALUES (12, 6, 7, '2022-07-15', 0);
INSERT INTO dm_participants VALUES (13, 7, 8, '2023-01-10', 0);
INSERT INTO dm_participants VALUES (14, 7, 9, '2023-01-10', 0);
INSERT INTO dm_participants VALUES (15, 8, 10, '2023-05-01', 0);
INSERT INTO dm_participants VALUES (16, 8, 7, '2023-05-01', 0);

-- =============================================
-- dm_messages (20 rows)
-- =============================================
CREATE TABLE dm_messages (
    id INTEGER PRIMARY KEY,
    thread_id INTEGER NOT NULL REFERENCES dm_threads(id),
    sender_id INTEGER NOT NULL REFERENCES accounts(id),
    message_text TEXT,
    media_url TEXT,
    sent_at TEXT NOT NULL,
    read_at TEXT,
    is_deleted INTEGER NOT NULL DEFAULT 0
);

INSERT INTO dm_messages VALUES (1, 1, 1, 'Hey Bob! How is the new recipe going?', NULL, '2024-03-01', '2024-03-01', 0);
INSERT INTO dm_messages VALUES (2, 1, 2, 'Great! Just perfected the sourdough', NULL, '2024-03-01', '2024-03-02', 0);
INSERT INTO dm_messages VALUES (3, 1, 1, 'Send me photos!', NULL, '2024-04-10', '2024-04-10', 0);
INSERT INTO dm_messages VALUES (4, 2, 1, 'Carol, want to plan a trip together?', NULL, '2024-02-20', '2024-02-20', 0);
INSERT INTO dm_messages VALUES (5, 2, 3, 'Yes! I was thinking about Japan', NULL, '2024-02-21', '2024-02-21', 0);
INSERT INTO dm_messages VALUES (6, 2, 1, 'Perfect! Let me send you my itinerary', '/media/msg/alice_itinerary.pdf', '2024-03-25', '2024-03-25', 0);
INSERT INTO dm_messages VALUES (7, 3, 2, 'Eve, love your latest artwork!', NULL, '2024-03-15', '2024-03-15', 0);
INSERT INTO dm_messages VALUES (8, 3, 5, 'Thanks Bob! Working on a new series', NULL, '2024-03-16', '2024-03-16', 0);
INSERT INTO dm_messages VALUES (9, 3, 5, 'Here is a sneak peek', '/media/msg/eve_preview.jpg', '2024-04-05', '2024-04-05', 0);
INSERT INTO dm_messages VALUES (10, 4, 3, 'Dave, any trail recommendations?', NULL, '2024-02-10', '2024-02-10', 0);
INSERT INTO dm_messages VALUES (11, 4, 4, 'Check out the Maroon Bells loop!', NULL, '2024-02-11', '2024-02-11', 0);
INSERT INTO dm_messages VALUES (12, 4, 3, 'Added to my list!', NULL, '2024-03-15', '2024-03-15', 0);
INSERT INTO dm_messages VALUES (13, 5, 4, 'Frank, want to hit the gym Saturday?', NULL, '2024-02-15', '2024-02-15', 0);
INSERT INTO dm_messages VALUES (14, 5, 6, 'Count me in! 8am?', NULL, '2024-02-15', '2024-02-16', 0);
INSERT INTO dm_messages VALUES (15, 5, 4, 'Perfect, see you there', NULL, '2024-02-28', '2024-02-28', 0);
INSERT INTO dm_messages VALUES (16, 6, 5, 'Grace, have you seen the new Villeneuve film?', NULL, '2024-03-20', '2024-03-20', 0);
INSERT INTO dm_messages VALUES (17, 6, 7, 'Not yet! Want to go this weekend?', NULL, '2024-03-21', '2024-03-21', 0);
INSERT INTO dm_messages VALUES (18, 7, 8, 'Ivy, any meditation app recommendations?', NULL, '2024-03-10', '2024-03-10', 0);
INSERT INTO dm_messages VALUES (19, 7, 9, 'Try Headspace or Calm - both are great!', NULL, '2024-03-20', '2024-03-20', 0);
INSERT INTO dm_messages VALUES (20, 8, 10, 'Grace, want to review my new track?', '/media/msg/jack_demo.mp3', '2024-04-08', NULL, 0);

-- =============================================
-- events (6 rows)
-- =============================================
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    creator_id INTEGER NOT NULL REFERENCES accounts(id),
    event_name TEXT NOT NULL,
    description TEXT,
    location TEXT,
    start_time TEXT NOT NULL,
    end_time TEXT,
    privacy TEXT NOT NULL DEFAULT 'public',
    cover_url TEXT,
    created_at TEXT NOT NULL,
    is_cancelled INTEGER NOT NULL DEFAULT 0
);

INSERT INTO events VALUES (1, 1, 'Tech Meetup 2024', 'Monthly technology meetup and networking', 'San Francisco Convention Center', '2024-03-15 18:00', '2024-03-15 21:00', 'public', NULL, '2024-02-01', 0);
INSERT INTO events VALUES (2, 2, 'Cooking Workshop', 'Learn to make authentic Italian pasta', 'Community Kitchen Austin', '2024-04-10 14:00', '2024-04-10 17:00', 'public', NULL, '2024-03-01', 0);
INSERT INTO events VALUES (3, 3, 'Photo Walk', 'Street photography walk through downtown', 'Pike Place Market Seattle', '2024-04-20 10:00', '2024-04-20 13:00', 'public', NULL, '2024-03-10', 0);
INSERT INTO events VALUES (4, 4, 'Fitness Bootcamp', 'High intensity outdoor workout', 'City Park Denver', '2024-05-01 06:00', '2024-05-01 08:00', 'private', NULL, '2024-03-20', 0);
INSERT INTO events VALUES (5, 5, 'Art Exhibition Opening', 'Digital art exhibition featuring local artists', 'Miami Art Gallery', '2024-05-15 19:00', '2024-05-15 22:00', 'public', NULL, '2024-04-01', 0);
INSERT INTO events VALUES (6, 10, 'Live Music Night', 'Acoustic live performance', 'Nashville Music Hall', '2024-06-01 20:00', '2024-06-01 23:00', 'public', NULL, '2024-04-15', 0);

-- =============================================
-- event_attendees (15 rows)
-- =============================================
CREATE TABLE event_attendees (
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(id),
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    rsvp_status TEXT NOT NULL DEFAULT 'invited',
    responded_at TEXT
);

INSERT INTO event_attendees VALUES (1, 1, 1, 'going', '2024-02-05');
INSERT INTO event_attendees VALUES (2, 1, 8, 'going', '2024-02-10');
INSERT INTO event_attendees VALUES (3, 1, 6, 'maybe', '2024-02-12');
INSERT INTO event_attendees VALUES (4, 2, 2, 'going', '2024-03-05');
INSERT INTO event_attendees VALUES (5, 2, 1, 'going', '2024-03-10');
INSERT INTO event_attendees VALUES (6, 2, 3, 'interested', '2024-03-12');
INSERT INTO event_attendees VALUES (7, 3, 3, 'going', '2024-03-15');
INSERT INTO event_attendees VALUES (8, 3, 1, 'interested', '2024-03-18');
INSERT INTO event_attendees VALUES (9, 4, 4, 'going', '2024-03-25');
INSERT INTO event_attendees VALUES (10, 4, 6, 'going', '2024-03-28');
INSERT INTO event_attendees VALUES (11, 5, 5, 'going', '2024-04-05');
INSERT INTO event_attendees VALUES (12, 5, 7, 'going', '2024-04-08');
INSERT INTO event_attendees VALUES (13, 5, 1, 'maybe', '2024-04-10');
INSERT INTO event_attendees VALUES (14, 6, 10, 'going', '2024-04-20');
INSERT INTO event_attendees VALUES (15, 6, 2, 'going', '2024-04-25');

-- =============================================
-- event_posts (6 rows)
-- =============================================
CREATE TABLE event_posts (
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(id),
    author_id INTEGER NOT NULL REFERENCES accounts(id),
    content TEXT NOT NULL,
    media_url TEXT,
    created_at TEXT NOT NULL
);

INSERT INTO event_posts VALUES (1, 1, 1, 'Excited to host tonight! See you all there', NULL, '2024-03-15');
INSERT INTO event_posts VALUES (2, 2, 2, 'Prep work done, ready for the workshop!', '/media/events/bob_prep.jpg', '2024-04-10');
INSERT INTO event_posts VALUES (3, 3, 3, 'Perfect weather for our photo walk today', NULL, '2024-04-20');
INSERT INTO event_posts VALUES (4, 4, 4, 'Bootcamp starts in 30 minutes, let us go!', NULL, '2024-05-01');
INSERT INTO event_posts VALUES (5, 5, 5, 'The exhibition is now open, welcome everyone!', '/media/events/eve_exhibition.jpg', '2024-05-15');
INSERT INTO event_posts VALUES (6, 6, 10, 'Sound check done, show starts at 8!', NULL, '2024-06-01');

-- =============================================
-- content_reports (6 rows)
-- =============================================
CREATE TABLE content_reports (
    id INTEGER PRIMARY KEY,
    reporter_id INTEGER NOT NULL REFERENCES accounts(id),
    content_type TEXT NOT NULL,
    content_id INTEGER NOT NULL,
    reason TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TEXT NOT NULL,
    reviewed_at TEXT,
    reviewer_notes TEXT
);

INSERT INTO content_reports VALUES (1, 1, 'post', 16, 'Inappropriate content', 'reviewed', '2024-04-01', NULL, NULL);
INSERT INTO content_reports VALUES (2, 2, 'comment', 10, 'Spam', 'pending', '2024-02-01', NULL, NULL);
INSERT INTO content_reports VALUES (3, 3, 'post', 12, 'Misleading information', 'reviewed', '2024-03-28', NULL, NULL);
INSERT INTO content_reports VALUES (4, 4, 'comment', 6, 'Harassment', 'pending', '2024-01-25', NULL, NULL);
INSERT INTO content_reports VALUES (5, 5, 'post', 4, 'Copyright violation', 'dismissed', '2024-03-15', NULL, NULL);
INSERT INTO content_reports VALUES (6, 6, 'comment', 22, 'Hate speech', 'pending', '2024-03-10', NULL, NULL);

-- =============================================
-- moderation_actions (6 rows)
-- =============================================
CREATE TABLE moderation_actions (
    id INTEGER PRIMARY KEY,
    report_id INTEGER NOT NULL REFERENCES content_reports(id),
    action_type TEXT NOT NULL DEFAULT 'review',
    action_by TEXT NOT NULL DEFAULT 'system',
    notes TEXT,
    created_at TEXT NOT NULL
);

INSERT INTO moderation_actions VALUES (1, 1, 'review', 'system', 'Content reviewed and flagged', '2024-04-02');
INSERT INTO moderation_actions VALUES (2, 2, 'review', 'system', 'Pending manual review', '2024-02-02');
INSERT INTO moderation_actions VALUES (3, 3, 'review', 'system', 'Content reviewed and removed', '2024-03-29');
INSERT INTO moderation_actions VALUES (4, 4, 'review', 'system', 'Pending manual review', '2024-01-26');
INSERT INTO moderation_actions VALUES (5, 5, 'dismiss', 'system', 'Report dismissed after review', '2024-03-16');
INSERT INTO moderation_actions VALUES (6, 6, 'review', 'system', 'Pending manual review', '2024-03-11');

-- =============================================
-- activity_log (15 rows)
-- =============================================
CREATE TABLE activity_log (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    activity_type TEXT NOT NULL,
    description TEXT,
    target_type TEXT,
    target_id INTEGER,
    ip_address TEXT,
    created_at TEXT NOT NULL
);

INSERT INTO activity_log VALUES (1, 1, 'login', 'Logged in from Chrome on macOS', 'session', NULL, NULL, '2024-04-10');
INSERT INTO activity_log VALUES (2, 1, 'post_create', 'Created a new photo post', 'post', 1, NULL, '2024-01-15');
INSERT INTO activity_log VALUES (3, 2, 'login', 'Logged in from Safari on iOS', 'session', NULL, NULL, '2024-04-08');
INSERT INTO activity_log VALUES (4, 2, 'post_create', 'Created a new photo post', 'post', 3, NULL, '2024-01-20');
INSERT INTO activity_log VALUES (5, 3, 'login', 'Logged in from Firefox on Windows', 'session', NULL, NULL, '2024-04-05');
INSERT INTO activity_log VALUES (6, 3, 'profile_update', 'Updated bio and avatar', 'profile', 3, NULL, '2024-03-20');
INSERT INTO activity_log VALUES (7, 4, 'login', 'Logged in from Chrome on Android', 'session', NULL, NULL, '2024-04-01');
INSERT INTO activity_log VALUES (8, 5, 'post_create', 'Created a new art post', 'post', 9, NULL, '2024-02-10');
INSERT INTO activity_log VALUES (9, 6, 'login', 'Logged in from Edge on Windows', 'session', NULL, NULL, '2024-03-28');
INSERT INTO activity_log VALUES (10, 7, 'post_create', 'Created a new text post', 'post', 13, NULL, '2024-02-15');
INSERT INTO activity_log VALUES (11, 8, 'login', 'Logged in from Chrome on macOS', 'session', NULL, NULL, '2024-03-25');
INSERT INTO activity_log VALUES (12, 9, 'post_create', 'Created a new photo post', 'post', 17, NULL, '2024-03-01');
INSERT INTO activity_log VALUES (13, 10, 'login', 'Logged in from Safari on macOS', 'session', NULL, NULL, '2024-04-12');
INSERT INTO activity_log VALUES (14, 10, 'post_create', 'Created a new link post', 'post', 19, NULL, '2024-03-05');
INSERT INTO activity_log VALUES (15, 1, 'settings_change', 'Updated privacy settings', 'settings', NULL, NULL, '2024-02-01');

-- =============================================
-- notification_preferences (10 rows)
-- =============================================
CREATE TABLE notification_preferences (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    likes_notify INTEGER NOT NULL DEFAULT 1,
    comments_notify INTEGER NOT NULL DEFAULT 1,
    follows_notify INTEGER NOT NULL DEFAULT 1,
    dm_notify INTEGER NOT NULL DEFAULT 1,
    mentions_notify INTEGER NOT NULL DEFAULT 1
);

INSERT INTO notification_preferences VALUES (1, 1, 1, 1, 1, 1, 1);
INSERT INTO notification_preferences VALUES (2, 2, 1, 1, 1, 1, 1);
INSERT INTO notification_preferences VALUES (3, 3, 1, 1, 1, 1, 1);
INSERT INTO notification_preferences VALUES (4, 4, 1, 1, 1, 1, 1);
INSERT INTO notification_preferences VALUES (5, 5, 1, 1, 1, 1, 1);
INSERT INTO notification_preferences VALUES (6, 6, 1, 1, 1, 1, 1);
INSERT INTO notification_preferences VALUES (7, 7, 1, 1, 1, 1, 1);
INSERT INTO notification_preferences VALUES (8, 8, 1, 1, 1, 1, 1);
INSERT INTO notification_preferences VALUES (9, 9, 1, 1, 1, 1, 1);
INSERT INTO notification_preferences VALUES (10, 10, 1, 1, 1, 1, 1);

-- =============================================
-- notifications (20 rows)
-- =============================================
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    notification_type TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    is_read INTEGER NOT NULL DEFAULT 0,
    source_type TEXT,
    source_id INTEGER,
    created_at TEXT NOT NULL
);

INSERT INTO notifications VALUES (1, 1, 'like', 'New Like', 'Bob liked your post', 1, 'like', 1, '2024-01-15');
INSERT INTO notifications VALUES (2, 1, 'comment', 'New Comment', 'Carol commented on your post', 1, 'comment', 2, '2024-01-15');
INSERT INTO notifications VALUES (3, 2, 'like', 'New Like', 'Alice liked your post', 1, 'like', 4, '2024-01-20');
INSERT INTO notifications VALUES (4, 3, 'comment', 'New Comment', 'Alice commented on your post', 1, 'comment', 7, '2024-02-05');
INSERT INTO notifications VALUES (5, 4, 'like', 'New Like', 'Frank liked your post', 1, 'like', 8, '2024-01-25');
INSERT INTO notifications VALUES (6, 5, 'like', 'New Like', 'Grace liked your post', 0, 'like', 9, '2024-02-10');
INSERT INTO notifications VALUES (7, 5, 'comment', 'New Comment', 'Grace commented on your art', 1, 'comment', 11, '2024-02-10');
INSERT INTO notifications VALUES (8, 6, 'like', 'New Like', 'Jack liked your post', 0, 'like', 11, '2024-01-30');
INSERT INTO notifications VALUES (9, 7, 'like', 'New Like', 'Alice liked your post', 1, 'like', 12, '2024-02-15');
INSERT INTO notifications VALUES (10, 8, 'comment', 'New Comment', 'Carol commented on your post', 1, 'comment', 16, '2024-02-28');
INSERT INTO notifications VALUES (11, 9, 'like', 'New Like', 'Bob liked your post', 0, 'like', 14, '2024-03-01');
INSERT INTO notifications VALUES (12, 9, 'comment', 'New Comment', 'Alice commented on your post', 1, 'comment', 18, '2024-03-01');
INSERT INTO notifications VALUES (13, 10, 'like', 'New Like', 'Grace liked your post', 1, 'like', 16, '2024-03-05');
INSERT INTO notifications VALUES (14, 10, 'comment', 'New Comment', 'Bob commented on your song post', 0, 'comment', 20, '2024-03-05');
INSERT INTO notifications VALUES (15, 1, 'friend_request', 'Follow Request', 'Henry sent you a friend request', 1, 'friend_request', NULL, '2022-01-10');
INSERT INTO notifications VALUES (16, 2, 'event', 'Event Invite', 'You are invited to Cooking Workshop', 0, 'event', 2, '2024-03-01');
INSERT INTO notifications VALUES (17, 3, 'group', 'Community Update', 'New post in Travel Bugs', 1, 'group', 7, '2024-03-10');
INSERT INTO notifications VALUES (18, 4, 'friend_request', 'Follow Request', 'Eve wants to connect', 0, 'friend_request', NULL, '2023-06-15');
INSERT INTO notifications VALUES (19, 5, 'page', 'Creator Update', 'Your page Eve Design Studio got a new follower', 1, 'page', 4, '2022-08-01');
INSERT INTO notifications VALUES (20, 6, 'group', 'Community Update', 'New post in Tech Enthusiasts', 0, 'group', 3, '2024-03-05');

-- =============================================
-- account_stats (10 rows) - COMPUTED
-- =============================================
CREATE TABLE account_stats (
    id INTEGER PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    post_count INTEGER NOT NULL DEFAULT 0,
    follower_count INTEGER NOT NULL DEFAULT 0,
    following_count INTEGER NOT NULL DEFAULT 0,
    total_likes_received INTEGER NOT NULL DEFAULT 0
);

-- account 1 (alice): 2 posts (1,2), followers: account 8,11->1 = 1 follower (id 11 = account 8 follows 1), following: 1->2,1->3,1->4 = 3, likes on posts 1,2: post1=3 likes, post2=0 likes = 3
-- account 2 (bob): 2 posts (3,4), followers: 1->2, 12(pending so count)=1+1=2, following: 2->3, 2->5 = 2, likes on post3=2, post4=0 = 2
-- account 3 (carol): 2 posts (5,6), followers: 2->3, 10->3 = 2, following: 3->6 = 1, likes on post5=2, post6=0 = 2
-- account 4 (dave): 2 posts (7,8), followers: 1->4 = 1, following: 4->7, 4->6 = 2, likes on post7=1, post8=0 = 1
-- account 5 (eve): 2 posts (9,10), followers: 2->5, 5->7(no, 15=5->7) = 1, following: 5->8, 5->7 = 2, likes on post9=2, post10=0 = 2
-- account 6 (frank): 2 posts (11,12), followers: 3->6, 4->6 = 2, following: 6->9 = 1, likes on post11=1, post12=0 = 1
-- account 7 (grace): 2 posts (13,14), followers: 4->7, 5->7 = 2, following: 7->10 = 1, likes on post13=1, post14=0 = 1
-- account 8 (henry): 2 posts (15,16), followers: 5->8 = 1, following: 8->1 = 1, likes on post15=1, post16=0 = 1
-- account 9 (ivy): 2 posts (17,18), followers: 6->9 = 1, following: 9->2 = 1, likes on post17=2, post18=0 = 2
-- account 10 (jack): 2 posts (19,20), followers: 7->10 = 1, following: 10->3 = 1, likes on post19=2, post20=1 = 3

INSERT INTO account_stats VALUES (1, 1, 2, 1, 3, 3);
INSERT INTO account_stats VALUES (2, 2, 2, 2, 2, 2);
INSERT INTO account_stats VALUES (3, 3, 2, 2, 1, 2);
INSERT INTO account_stats VALUES (4, 4, 2, 1, 2, 1);
INSERT INTO account_stats VALUES (5, 5, 2, 1, 2, 2);
INSERT INTO account_stats VALUES (6, 6, 2, 2, 1, 1);
INSERT INTO account_stats VALUES (7, 7, 2, 2, 1, 1);
INSERT INTO account_stats VALUES (8, 8, 2, 1, 1, 1);
INSERT INTO account_stats VALUES (9, 9, 2, 1, 1, 2);
INSERT INTO account_stats VALUES (10, 10, 2, 1, 1, 3);

-- =============================================
-- post_analytics (20 rows) - COMPUTED
-- =============================================
CREATE TABLE post_analytics (
    id INTEGER PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES media_posts(id),
    like_count INTEGER NOT NULL DEFAULT 0,
    comment_count INTEGER NOT NULL DEFAULT 0,
    share_count INTEGER NOT NULL DEFAULT 0,
    save_count INTEGER NOT NULL DEFAULT 0,
    view_count INTEGER NOT NULL DEFAULT 0
);

-- post 1: 3 likes (ids 1,2,3), 3 comments (ids 1,2,3), 1 share, 1 save (id 3), views=50
-- post 2: 0 likes, 0 comments, 0 shares, 0 saves, views=20
-- post 3: 2 likes (ids 4,5), 3 comments (ids 4,5,6), 0 shares, 1 save (id 9), views=45
-- post 4: 0 likes, 0 comments, 0 shares, 0 saves, views=15
-- post 5: 2 likes (ids 6,7), 2 comments (ids 7,8), 1 share, 1 save (id 1), views=60
-- post 6: 0 likes, 0 comments, 0 shares, 0 saves, views=25
-- post 7: 1 like (id 8), 2 comments (ids 9,10), 0 shares, 1 save (id 5), views=35
-- post 8: 0 likes, 1 comment (id 24), 0 shares, 0 saves, views=30
-- post 9: 2 likes (ids 9,10), 2 comments (ids 11,12), 1 share, 2 saves (ids 2,8), views=55
-- post 10: 0 likes, 1 comment (id 23), 0 shares, 0 saves, views=40
-- post 11: 1 like (id 11), 1 comment (id 13), 0 shares, 0 saves, views=30
-- post 12: 0 likes, 0 comments, 0 shares, 0 saves, views=10
-- post 13: 1 like (id 12), 2 comments (ids 14,15), 0 shares, 1 save (id 10), views=45
-- post 14: 0 likes, 0 comments, 0 shares, 0 saves, views=20
-- post 15: 1 like (id 13), 2 comments (ids 16,17), 0 shares, 1 save (id 7), views=50
-- post 16: 0 likes, 0 comments, 0 shares, 0 saves, views=10
-- post 17: 2 likes (ids 14,15), 2 comments (ids 18,19), 1 share, 1 save (id 4), views=65
-- post 18: 0 likes, 0 comments, 0 shares, 0 saves, views=30
-- post 19: 2 likes (ids 16,17), 3 comments (ids 20,21,22), 1 share, 1 save (id 6), views=70
-- post 20: 1 like (id 18), 1 comment (id 25), 0 shares, 0 saves, views=(1+1)*10=20

INSERT INTO post_analytics VALUES (1, 1, 3, 3, 1, 1, 60);
INSERT INTO post_analytics VALUES (2, 2, 0, 0, 0, 0, 0);
INSERT INTO post_analytics VALUES (3, 3, 2, 3, 0, 1, 50);
INSERT INTO post_analytics VALUES (4, 4, 0, 0, 0, 0, 0);
INSERT INTO post_analytics VALUES (5, 5, 2, 2, 1, 1, 40);
INSERT INTO post_analytics VALUES (6, 6, 0, 0, 0, 0, 0);
INSERT INTO post_analytics VALUES (7, 7, 1, 2, 0, 1, 30);
INSERT INTO post_analytics VALUES (8, 8, 0, 1, 0, 0, 10);
INSERT INTO post_analytics VALUES (9, 9, 2, 2, 1, 2, 40);
INSERT INTO post_analytics VALUES (10, 10, 0, 1, 0, 0, 10);
INSERT INTO post_analytics VALUES (11, 11, 1, 1, 0, 0, 20);
INSERT INTO post_analytics VALUES (12, 12, 0, 0, 0, 0, 0);
INSERT INTO post_analytics VALUES (13, 13, 1, 2, 0, 1, 30);
INSERT INTO post_analytics VALUES (14, 14, 0, 0, 0, 0, 0);
INSERT INTO post_analytics VALUES (15, 15, 1, 2, 0, 1, 30);
INSERT INTO post_analytics VALUES (16, 16, 0, 0, 0, 0, 0);
INSERT INTO post_analytics VALUES (17, 17, 2, 2, 1, 1, 40);
INSERT INTO post_analytics VALUES (18, 18, 0, 0, 0, 0, 0);
INSERT INTO post_analytics VALUES (19, 19, 2, 3, 1, 1, 50);
INSERT INTO post_analytics VALUES (20, 20, 1, 1, 0, 0, 20);

-- =============================================
-- engagement_daily (4 rows) - COMPUTED
-- =============================================
CREATE TABLE engagement_daily (
    id INTEGER PRIMARY KEY,
    summary_date TEXT NOT NULL,
    total_posts INTEGER NOT NULL DEFAULT 0,
    total_likes INTEGER NOT NULL DEFAULT 0,
    total_comments INTEGER NOT NULL DEFAULT 0,
    total_new_accounts INTEGER NOT NULL DEFAULT 0
);

INSERT INTO engagement_daily VALUES (1, '2024-01', 4, 7, 9, 0);
INSERT INTO engagement_daily VALUES (2, '2024-02', 5, 6, 7, 0);
INSERT INTO engagement_daily VALUES (3, '2024-03', 6, 4, 7, 0);
INSERT INTO engagement_daily VALUES (4, '2024-04', 5, 1, 2, 0);

-- =============================================
-- hashtag_trends (8 rows) - COMPUTED
-- =============================================
CREATE TABLE hashtag_trends (
    id INTEGER PRIMARY KEY,
    hashtag_id INTEGER NOT NULL REFERENCES hashtags(id),
    period TEXT NOT NULL,
    post_count INTEGER NOT NULL DEFAULT 0,
    engagement_score REAL NOT NULL DEFAULT 0.0
);

INSERT INTO hashtag_trends VALUES (1, 1, '2024-Q1', 3, 7.5);
INSERT INTO hashtag_trends VALUES (2, 2, '2024-Q1', 2, 5.0);
INSERT INTO hashtag_trends VALUES (3, 3, '2024-Q1', 3, 7.5);
INSERT INTO hashtag_trends VALUES (4, 4, '2024-Q1', 2, 5.0);
INSERT INTO hashtag_trends VALUES (5, 5, '2024-Q1', 2, 5.0);
INSERT INTO hashtag_trends VALUES (6, 6, '2024-Q1', 1, 2.5);
INSERT INTO hashtag_trends VALUES (7, 7, '2024-Q1', 1, 2.5);
INSERT INTO hashtag_trends VALUES (8, 8, '2024-Q1', 1, 2.5);

-- =============================================
-- community_stats (6 rows) - COMPUTED
-- =============================================
CREATE TABLE community_stats (
    id INTEGER PRIMARY KEY,
    community_id INTEGER NOT NULL REFERENCES communities(id),
    total_posts INTEGER NOT NULL DEFAULT 0,
    total_members INTEGER NOT NULL DEFAULT 0,
    active_members INTEGER NOT NULL DEFAULT 0
);

INSERT INTO community_stats VALUES (1, 1, 3, 5, 3);
INSERT INTO community_stats VALUES (2, 2, 2, 4, 2);
INSERT INTO community_stats VALUES (3, 3, 2, 3, 2);
INSERT INTO community_stats VALUES (4, 4, 2, 3, 2);
INSERT INTO community_stats VALUES (5, 5, 2, 2, 2);
INSERT INTO community_stats VALUES (6, 6, 1, 1, 1);

-- =============================================
-- migration_log (25 rows)
-- =============================================
CREATE TABLE migration_log (
    id INTEGER PRIMARY KEY,
    source_table TEXT NOT NULL,
    target_table TEXT NOT NULL,
    rows_migrated INTEGER NOT NULL DEFAULT 0,
    migrated_at TEXT NOT NULL
);

INSERT INTO migration_log VALUES (1, 'fb_users', 'accounts', 10, '2024-04-15 10:00:00');
INSERT INTO migration_log VALUES (2, 'fb_profiles', 'profiles', 10, '2024-04-15 10:01:00');
INSERT INTO migration_log VALUES (3, 'fb_privacy_settings', 'account_settings', 10, '2024-04-15 10:02:00');
INSERT INTO migration_log VALUES (4, 'fb_friendships', 'follow_relationships', 15, '2024-04-15 10:03:00');
INSERT INTO migration_log VALUES (5, 'fb_blocked_users', 'blocked_accounts', 5, '2024-04-15 10:04:00');
INSERT INTO migration_log VALUES (6, 'fb_users', 'account_verifications', 10, '2024-04-15 10:05:00');
INSERT INTO migration_log VALUES (7, 'fb_posts', 'media_posts', 20, '2024-04-15 10:06:00');
INSERT INTO migration_log VALUES (8, 'fb_comments', 'post_comments', 25, '2024-04-15 10:07:00');
INSERT INTO migration_log VALUES (9, 'fb_likes', 'post_likes', 18, '2024-04-15 10:08:00');
INSERT INTO migration_log VALUES (10, 'fb_likes', 'comment_likes', 12, '2024-04-15 10:09:00');
INSERT INTO migration_log VALUES (11, 'fb_saved_items', 'saved_posts', 10, '2024-04-15 10:10:00');
INSERT INTO migration_log VALUES (12, 'fb_albums', 'media_albums', 8, '2024-04-15 10:11:00');
INSERT INTO migration_log VALUES (13, 'fb_photos', 'album_media', 8, '2024-04-15 10:12:00');
INSERT INTO migration_log VALUES (14, 'fb_hashtags', 'hashtags', 8, '2024-04-15 10:13:00');
INSERT INTO migration_log VALUES (15, 'fb_post_hashtags', 'post_hashtags', 15, '2024-04-15 10:14:00');
INSERT INTO migration_log VALUES (16, 'fb_posts', 'post_mentions', 6, '2024-04-15 10:15:00');
INSERT INTO migration_log VALUES (17, 'fb_posts', 'post_shares', 5, '2024-04-15 10:16:00');
INSERT INTO migration_log VALUES (18, 'fb_posts', 'stories', 5, '2024-04-15 10:17:00');
INSERT INTO migration_log VALUES (19, 'fb_groups', 'communities', 6, '2024-04-15 10:18:00');
INSERT INTO migration_log VALUES (20, 'fb_group_members', 'community_members', 18, '2024-04-15 10:19:00');
INSERT INTO migration_log VALUES (21, 'fb_group_posts', 'community_posts', 12, '2024-04-15 10:20:00');
INSERT INTO migration_log VALUES (22, 'fb_pages', 'creator_accounts', 5, '2024-04-15 10:21:00');
INSERT INTO migration_log VALUES (23, 'fb_page_followers', 'creator_followers', 12, '2024-04-15 10:22:00');
INSERT INTO migration_log VALUES (24, 'fb_conversations', 'dm_threads', 8, '2024-04-15 10:23:00');
INSERT INTO migration_log VALUES (25, 'fb_messages', 'dm_messages', 20, '2024-04-15 10:24:00');
"""
