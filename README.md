# Follio Django Portfolio

This project turns the bundled `Follio` Bootstrap template into a Django site with admin-managed content.

The frontend now supports `en`, `ru`, and `uz`, and content models include language-specific fields for translated text.

## Run locally

Use the helper script:

```powershell
.\manage.cmd runserver
```

Useful commands:

```powershell
.\manage.cmd migrate
.\manage.cmd test
.\manage.cmd check
```

## Admin

Open:

```text
http://127.0.0.1:8000/admin/
```

Local superuser:

- Username: `admin`
- Password: `admin12345`

Change the password after login if needed.

## What is editable from admin

- Site settings
- Social links
- Skills
- Services
- Awards
- Projects
- Testimonials
- Blog posts
- Contact messages

Language switching is available from the site header.

Images can now be uploaded from admin as well. If an upload field is left empty, the site automatically falls back to the existing static asset path for that item.

## SEO

The site now includes:

- `sitemap.xml` with static pages, projects, and published blog posts
- `robots.txt` with a sitemap reference
- canonical URLs
- Open Graph and Twitter meta tags
- JSON-LD structured data for the website, profile, pages, projects, and blog posts

## Telegram bot notification

If you want each new contact form submission to also be sent to Telegram, set these environment variables before starting Django:

```powershell
$env:TELEGRAM_BOT_TOKEN="123456:ABCDEF"
$env:TELEGRAM_CHAT_ID="-1001234567890"
.\manage.cmd runserver
```

Without these variables, contact messages will still be saved in Django admin as usual.
