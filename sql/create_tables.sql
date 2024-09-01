CREATE TABLE `Page` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`url` text NOT NULL,
	`title` text
);

CREATE TABLE `PageHighlights` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`savedAt` integer DEFAULT (unixepoch()) NOT NULL,
	`highlight` text NOT NULL,
	`highlightText` text,
	`pageId` integer,
	FOREIGN KEY (`pageId`) REFERENCES `Page`(`id`) ON UPDATE cascade ON DELETE restrict
);

CREATE TABLE `PageSaves` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`savedAt` integer DEFAULT (unixepoch()) NOT NULL,
	`saveType` text,
	`pageId` integer,
	FOREIGN KEY (`pageId`) REFERENCES `Page`(`id`) ON UPDATE cascade ON DELETE restrict
);

CREATE UNIQUE INDEX `Page_url_unique` ON `Page` (`url`);

