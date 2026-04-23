# Google Sheet Schema

The spreadsheet must contain exactly **four tabs** with the names below.
Column headers (first row) must match exactly — they become JSON field names.

---

## Tab: `items`

| Column | Type | Required | Notes |
|--------|------|----------|-------|
| id | text | ✅ | Unique. Format: `ITM-XXXX` |
| title | text | ✅ | Short display title |
| text | text | ✅ | Main dhikr / dua text (Arabic) |
| type | text | ✅ | One of: `ذكر يومي`, `ذكر تسبيح`, `دعاء`, `رقية`, `ورد`, `مقروء`, `صلاة على النبي`, `فائدة`, `مجرب`, `محتوى هجري` |
| sectionMain | text | ✅ | e.g. `أذكار المسلم` |
| sectionSub | text | | e.g. `أذكار الصباح` |
| status | text | ✅ | One of: `مأثور`, `مشهور`, `منقول`, `مجرب`, `خاص` |
| interaction | text | ✅ | One of: `قراءة فقط`, `عداد`, `قراءة مع إنجاز`, `تذكير فقط`, `تذكير + عداد` |
| defaultCount | number | | Default counter value (default: 1) |
| allowCustomCount | TRUE/FALSE | | |
| daleel | text | | Reference / evidence |
| source | text | | Book/collection source |
| benefit | text | | Benefit description |
| displayNotes | text | | Notes shown in UI |
| relatedAfterPrayer | TRUE/FALSE | | Show in after-prayer section |
| showInTasbeeh | TRUE/FALSE | | Show in tasbeeh counter |
| showInHome | TRUE/FALSE | | Show on home screen |
| order | number | | Sort order (lower = first) |
| isActive | TRUE/FALSE | | Set FALSE to hide without deleting |
| link | text | | Optional URL |

---

## Tab: `readings`

| Column | Type | Required | Notes |
|--------|------|----------|-------|
| id | text | ✅ | Unique. Format: `RD-XXXX` |
| title | text | ✅ | Reading title |
| type | text | ✅ | e.g. `حزب`, `ورد`, `سورة` |
| section | text | ✅ | e.g. `المقرؤات والأوراد` |
| description | text | | Short description |
| source | text | | |
| benefit | text | | |
| suggestedTime | text | | e.g. `بعد الفجر` |
| reminderEnabled | TRUE/FALSE | | |
| relatedAfterPrayer | TRUE/FALSE | | |
| order | number | | |
| isActive | TRUE/FALSE | | |
| segmentCount | number | | Total number of segments |
| estimatedMinutes | number | | Estimated reading time |
| link | text | | |
| notes | text | | |

---

## Tab: `segments`

| Column | Type | Required | Notes |
|--------|------|----------|-------|
| id | text | ✅ | Unique. Format: `SEG-XXXX` |
| readingId | text | ✅ | Must match an `id` in readings tab |
| segmentNumber | number | ✅ | 1-based |
| subtitle | text | | Section heading |
| text | text | ✅ | Segment text (Arabic) |
| explanation | text | | |
| benefit | text | | |
| shareable | TRUE/FALSE | | |
| hasIndependentCompletion | TRUE/FALSE | | |
| order | number | | |
| isActive | TRUE/FALSE | | |
| notes | text | | |

---

## Tab: `hijri_content`

| Column | Type | Required | Notes |
|--------|------|----------|-------|
| id | text | ✅ | Unique. Format: `HJ-XXXX` |
| hijriMonth | text | ✅ | Arabic month name, e.g. `رمضان` |
| hijriDay | number | ✅ | Day of month (1–30) |
| entryType | text | ✅ | One of: `مناسبة`, `حدث`, `فائدة` |
| title | text | ✅ | |
| whatHappened | text | | Historical event description |
| benefit | text | | |
| recommended | text | | Recommended acts |
| references | text | | |
| showInHome | TRUE/FALSE | | |
| showInWidget | TRUE/FALSE | | |
| priority | text | | `عالية`, `متوسطة`, `منخفضة` |
| order | number | | |
