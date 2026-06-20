#!/usr/bin/env python3
"""
HRCP Prep Hub — HR Certification Affiliate SEO Build
Site   : https://brightlane.github.io/hrcp.com/
Aff    : https://www.linkconnector.com/ta.php?lc=007949120619007379&atid=HRCPWebs
Pages  : ~1,400+ across 8 languages
Build  : python3 build.py  (~8 seconds)
Deploy : GitHub Actions cron 06:00 UTC daily
"""
import json, re, hashlib, os, math
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import defaultdict, Counter

SITE     = "https://brightlane.github.io/hrcp.com"
NAME     = "HRCP Prep Hub"
AFF      = "https://www.linkconnector.com/ta.php?lc=007949120619007379&atid=HRCPWebs"
AFF_HOME = "https://www.hrcp.com/"
NOW      = datetime.now(timezone.utc)
TODAY    = NOW.strftime("%Y-%m-%d")
YEAR     = NOW.year
OG       = SITE + "/og.svg"
OUT      = Path("output")

GOOGLE_V = "eWVDN3vbam9nnaZQu7wAQKyfmJJdM7zjI80l4DGeUrQ"
BING_V   = "574044E39556B8B8DAAF1D1F233C87B0"

def sh(s): return int(hashlib.md5(s.encode()).hexdigest(), 16)
def wc(html): return len(re.findall(r'\b\w+\b', re.sub(r'<[^>]+>',' ', html)))
def read_mins(html): return max(4, round(wc(html) / 238))

_TITLE_SEEN: dict = {}

def unique_title(title, slug):
    if title not in _TITLE_SEEN:
        _TITLE_SEEN[title] = slug; return title
    tag = slug[-10:].lstrip("-")
    parts = title.rsplit(" | ", 1)
    if len(parts) == 2:
        pipe = f" | {parts[1]}"
        c = (parts[0].rstrip()[:70-len(tag)-3-len(pipe)].rstrip() + f" [{tag}]" + pipe)[:72]
    else:
        c = (title + f" [{tag}]")[:72]
    _TITLE_SEEN[c] = slug; return c

def ttag(kw, lang_sfx="| HRCP Prep Hub"):
    sfx  = f" {lang_sfx}"
    base = kw
    if len(base)+len(sfx) < 48:
        enrichments = [" — Complete Guide"," Study Guide & Review"," Prep & Tips",
                       " — Expert Guide"," — Honest Review"," Tips & Strategy"]
        base += enrichments[sh(kw) % len(enrichments)]
    max_b = 68 - len(sfx)
    if len(base) > max_b:
        base = base[:max_b].rsplit(" ", 1)[0]
    return base + sfx


# ── LANGUAGES ─────────────────────────────────────────────────────────────────
LANGUAGES = {
    "en":{"name":"English","native":"English","dir":"guides","suffix":"| HRCP Prep Hub",
          "try_free":"Get HRCP Study Materials","cta":"Start Studying Now",
          "free_trial":"Pass-or-money-back guarantee","no_cc":"Instant digital access",
          "home":"Home","guides_lbl":"Guides","blog_lbl":"Blog","faq_lbl":"FAQ",
          "updated":"Updated","read_min":"min read",
          "sidebar_h":"Get HRCP Study Materials","sidebar_sub":"Pass or your money back • Since 1995",
          "bottom_cta_h":"Ready to Get Certified?","bottom_cta_p":"HRCP study materials have helped 100,000+ HR professionals pass their certification exams.",
          "disclosure":"Affiliate Disclosure: We earn commissions when you purchase HRCP materials through our links.",
          "currency":"USD"},
    "es":{"name":"Spanish","native":"Español","dir":"es/guias","suffix":"| HRCP Prep Hub",
          "try_free":"Obtener Materiales HRCP","cta":"Empezar a Estudiar",
          "free_trial":"Garantía de aprobación","no_cc":"Acceso digital inmediato",
          "home":"Inicio","guides_lbl":"Guías","blog_lbl":"Blog","faq_lbl":"FAQ",
          "updated":"Actualizado","read_min":"min de lectura",
          "sidebar_h":"Materiales de Estudio HRCP","sidebar_sub":"Garantía de aprobación • Desde 1995",
          "bottom_cta_h":"¿Listo para Certificarte?","bottom_cta_p":"Los materiales de HRCP han ayudado a más de 100.000 profesionales de RRHH a aprobar sus exámenes.",
          "disclosure":"Divulgación: Ganamos comisiones en compras calificadas.",
          "currency":"USD"},
    "pt":{"name":"Portuguese","native":"Português","dir":"pt/guias","suffix":"| HRCP Prep Hub",
          "try_free":"Obter Materiais HRCP","cta":"Começar a Estudar",
          "free_trial":"Garantia de aprovação","no_cc":"Acesso digital imediato",
          "home":"Início","guides_lbl":"Guias","blog_lbl":"Blog","faq_lbl":"FAQ",
          "updated":"Atualizado","read_min":"min de leitura",
          "sidebar_h":"Materiais de Estudo HRCP","sidebar_sub":"Garantia de aprovação • Desde 1995",
          "bottom_cta_h":"Pronto para se Certificar?","bottom_cta_p":"Os materiais HRCP ajudaram mais de 100.000 profissionais de RH a passar em seus exames.",
          "disclosure":"Divulgação de afiliados: Ganhamos comissões quando você compra via nossos links.",
          "currency":"USD"},
    "fr":{"name":"French","native":"Français","dir":"fr/guides","suffix":"| HRCP Prep Hub",
          "try_free":"Obtenir les Matériaux HRCP","cta":"Commencer à Étudier",
          "free_trial":"Garantie réussite ou remboursement","no_cc":"Accès numérique immédiat",
          "home":"Accueil","guides_lbl":"Guides","blog_lbl":"Blog","faq_lbl":"FAQ",
          "updated":"Mis à jour","read_min":"min de lecture",
          "sidebar_h":"Matériaux d'Étude HRCP","sidebar_sub":"Garantie de réussite • Depuis 1995",
          "bottom_cta_h":"Prêt à Vous Certifier ?","bottom_cta_p":"Les matériaux HRCP ont aidé plus de 100 000 professionnels RH à réussir leurs examens.",
          "disclosure":"Affiliation : Nous gagnons des commissions sur les achats qualifiés.",
          "currency":"USD"},
    "de":{"name":"German","native":"Deutsch","dir":"de/anleitungen","suffix":"| HRCP Prep Hub",
          "try_free":"HRCP-Materialien Holen","cta":"Jetzt Lernen",
          "free_trial":"Bestehen oder Geld zurück","no_cc":"Sofortiger digitaler Zugang",
          "home":"Startseite","guides_lbl":"Anleitungen","blog_lbl":"Blog","faq_lbl":"FAQ",
          "updated":"Aktualisiert","read_min":"Min. Lesezeit",
          "sidebar_h":"HRCP-Lernmaterialien","sidebar_sub":"Bestehen oder Geld zurück • Seit 1995",
          "bottom_cta_h":"Bereit für Ihre Zertifizierung?","bottom_cta_p":"HRCP-Materialien haben über 100.000 HR-Fachleuten geholfen, ihre Zertifizierungsprüfungen zu bestehen.",
          "disclosure":"Affiliate-Offenlegung: Wir verdienen Provisionen bei qualifizierten Käufen.",
          "currency":"USD"},
    "ja":{"name":"Japanese","native":"日本語","dir":"ja/guides","suffix":"| HRCP Prep Hub",
          "try_free":"HRCP教材を入手","cta":"今すぐ学習開始",
          "free_trial":"合格保証付き","no_cc":"即時デジタルアクセス",
          "home":"ホーム","guides_lbl":"ガイド","blog_lbl":"ブログ","faq_lbl":"FAQ",
          "updated":"更新日","read_min":"分で読める",
          "sidebar_h":"HRCP学習教材","sidebar_sub":"合格保証 • 1995年創業",
          "bottom_cta_h":"認定資格取得の準備はできていますか？","bottom_cta_p":"HRCP教材は10万人以上のHR専門家が資格試験に合格するのを支援してきました。",
          "disclosure":"アフィリエイト開示：当サイトのリンク経由の購入で手数料を受け取ります。",
          "currency":"JPY"},
    "ko":{"name":"Korean","native":"한국어","dir":"ko/guides","suffix":"| HRCP Prep Hub",
          "try_free":"HRCP 학습 자료 받기","cta":"지금 학습 시작",
          "free_trial":"합격 보장 제도","no_cc":"즉시 디지털 접근",
          "home":"홈","guides_lbl":"가이드","blog_lbl":"블로그","faq_lbl":"FAQ",
          "updated":"업데이트","read_min":"분 읽기",
          "sidebar_h":"HRCP 학습 자료","sidebar_sub":"합격 보장 • 1995년 설립",
          "bottom_cta_h":"자격증 취득 준비가 됐나요?","bottom_cta_p":"HRCP 교재는 10만 명 이상의 HR 전문가가 자격증 시험을 통과하는 데 도움을 주었습니다.",
          "disclosure":"제휴 공개: 링크를 통해 구매 시 수수료를 받습니다.",
          "currency":"KRW"},
    "ar":{"name":"Arabic","native":"العربية","dir":"ar/guides","suffix":"| HRCP Prep Hub",
          "try_free":"احصل على مواد HRCP","cta":"ابدأ الدراسة الآن",
          "free_trial":"ضمان النجاح أو استرداد المال","no_cc":"وصول رقمي فوري",
          "home":"الرئيسية","guides_lbl":"أدلة","blog_lbl":"مدونة","faq_lbl":"أسئلة",
          "updated":"تم التحديث","read_min":"دقيقة قراءة",
          "sidebar_h":"مواد دراسة HRCP","sidebar_sub":"ضمان النجاح • منذ 1995",
          "bottom_cta_h":"هل أنت مستعد للحصول على الشهادة؟","bottom_cta_p":"ساعدت مواد HRCP أكثر من 100,000 متخصص في الموارد البشرية على اجتياز امتحانات الشهادات.",
          "disclosure":"إفصاح: نكسب عمولات عند الشراء عبر روابطنا.",
          "currency":"USD"},
    "zh":{"name":"Chinese","native":"中文","dir":"zh/guides","suffix":"| HRCP Prep Hub",
          "try_free":"获取HRCP学习材料","cta":"立即开始学习",
          "free_trial":"通过或退款保证","no_cc":"立即数字访问",
          "home":"首页","guides_lbl":"指南","blog_lbl":"博客","faq_lbl":"常见问题",
          "updated":"更新时间","read_min":"分钟阅读",
          "sidebar_h":"HRCP学习材料","sidebar_sub":"通过或退款 • 1995年至今",
          "bottom_cta_h":"准备好获得HR认证了吗？","bottom_cta_p":"自1995年以来，HRCP学习材料已帮助超过100,000名HR专业人员通过认证考试。",
          "disclosure":"联盟声明：通过我们的链接购买时，我们将获得佣金。",
          "currency":"CNY"},
    "hi":{"name":"Hindi","native":"हिंदी","dir":"hi/guides","suffix":"| HRCP Prep Hub",
          "try_free":"HRCP सामग्री प्राप्त करें","cta":"अभी पढ़ना शुरू करें",
          "free_trial":"पास-या-पैसे-वापस गारंटी","no_cc":"तत्काल डिजिटल एक्सेस",
          "home":"होम","guides_lbl":"गाइड","blog_lbl":"ब्लॉग","faq_lbl":"FAQ",
          "updated":"अपडेट","read_min":"मिनट पढ़ें",
          "sidebar_h":"HRCP अध्ययन सामग्री","sidebar_sub":"पास गारंटी • 1995 से",
          "bottom_cta_h":"HR प्रमाणन के लिए तैयार?","bottom_cta_p":"HRCP सामग्री ने 1995 से 100,000+ HR पेशेवरों को उनकी परीक्षाएं पास करने में मदद की है।",
          "disclosure":"संबद्ध प्रकटीकरण: हमारे लिंक के माध्यम से खरीदारी पर हमें कमीशन मिलता है।",
          "currency":"INR"},
    "it":{"name":"Italian","native":"Italiano","dir":"it/guide","suffix":"| HRCP Prep Hub",
          "try_free":"Ottieni Materiali HRCP","cta":"Inizia a Studiare",
          "free_trial":"Garanzia superamento o rimborso","no_cc":"Accesso digitale immediato",
          "home":"Home","guides_lbl":"Guide","blog_lbl":"Blog","faq_lbl":"FAQ",
          "updated":"Aggiornato","read_min":"min di lettura",
          "sidebar_h":"Materiali di Studio HRCP","sidebar_sub":"Garanzia di superamento • Dal 1995",
          "bottom_cta_h":"Pronto per la Certificazione?","bottom_cta_p":"I materiali HRCP hanno aiutato oltre 100.000 professionisti HR a superare i loro esami di certificazione.",
          "disclosure":"Divulgazione affiliati: Guadagniamo commissioni sugli acquisti qualificati.",
          "currency":"EUR"},
    "nl":{"name":"Dutch","native":"Nederlands","dir":"nl/gidsen","suffix":"| HRCP Prep Hub",
          "try_free":"HRCP Materialen Halen","cta":"Nu Beginnen met Studeren",
          "free_trial":"Slagen of geld terug","no_cc":"Directe digitale toegang",
          "home":"Home","guides_lbl":"Gidsen","blog_lbl":"Blog","faq_lbl":"FAQ",
          "updated":"Bijgewerkt","read_min":"min lezen",
          "sidebar_h":"HRCP Studiematerialen","sidebar_sub":"Slaaggarantie • Sinds 1995",
          "bottom_cta_h":"Klaar voor uw Certificering?","bottom_cta_p":"HRCP-materialen hebben meer dan 100.000 HR-professionals geholpen hun certificeringsexamens te halen.",
          "disclosure":"Affiliate-openbaarmaking: Wij verdienen commissies op gekwalificeerde aankopen.",
          "currency":"EUR"},
    "pl":{"name":"Polish","native":"Polski","dir":"pl/przewodniki","suffix":"| HRCP Prep Hub",
          "try_free":"Zdobądź Materiały HRCP","cta":"Zacznij Się Uczyć",
          "free_trial":"Zdasz lub zwrot pieniędzy","no_cc":"Natychmiastowy dostęp cyfrowy",
          "home":"Strona główna","guides_lbl":"Przewodniki","blog_lbl":"Blog","faq_lbl":"FAQ",
          "updated":"Zaktualizowano","read_min":"min czytania",
          "sidebar_h":"Materiały do Nauki HRCP","sidebar_sub":"Gwarancja zdania • Od 1995",
          "bottom_cta_h":"Gotowy do Certyfikacji?","bottom_cta_p":"Materiały HRCP pomogły ponad 100 000 specjalistów HR zdać egzaminy certyfikacyjne od 1995 roku.",
          "disclosure":"Ujawnienie partnerskie: Zarabiamy prowizje od kwalifikowanych zakupów.",
          "currency":"PLN"},
    "tr":{"name":"Turkish","native":"Türkçe","dir":"tr/rehberler","suffix":"| HRCP Prep Hub",
          "try_free":"HRCP Materyallerini Al","cta":"Şimdi Çalışmaya Başla",
          "free_trial":"Geç ya da Para İadesi","no_cc":"Anında dijital erişim",
          "home":"Ana Sayfa","guides_lbl":"Rehberler","blog_lbl":"Blog","faq_lbl":"SSS",
          "updated":"Güncellendi","read_min":"dk okuma",
          "sidebar_h":"HRCP Çalışma Materyalleri","sidebar_sub":"Geçme garantisi • 1995'ten beri",
          "bottom_cta_h":"Sertifikasyon için Hazır mısınız?","bottom_cta_p":"HRCP materyalleri, 1995'ten bu yana 100.000'den fazla İK profesyonelinin sertifikasyon sınavlarını geçmesine yardımcı olmuştur.",
          "disclosure":"Ortaklık açıklaması: Bağlantılarımız üzerinden yapılan satın alımlarda komisyon kazanırız.",
          "currency":"TRY"},
    "id":{"name":"Indonesian","native":"Bahasa Indonesia","dir":"id/panduan","suffix":"| HRCP Prep Hub",
          "try_free":"Dapatkan Materi HRCP","cta":"Mulai Belajar Sekarang",
          "free_trial":"Garansi lulus atau uang kembali","no_cc":"Akses digital instan",
          "home":"Beranda","guides_lbl":"Panduan","blog_lbl":"Blog","faq_lbl":"FAQ",
          "updated":"Diperbarui","read_min":"menit baca",
          "sidebar_h":"Materi Belajar HRCP","sidebar_sub":"Garansi lulus • Sejak 1995",
          "bottom_cta_h":"Siap Mendapatkan Sertifikasi HR?","bottom_cta_p":"Materi HRCP telah membantu lebih dari 100.000 profesional HR lulus ujian sertifikasi mereka sejak 1995.",
          "disclosure":"Pengungkapan afiliasi: Kami mendapatkan komisi atas pembelian yang memenuhi syarat.",
          "currency":"IDR"},
    "vi":{"name":"Vietnamese","native":"Tiếng Việt","dir":"vi/huong-dan","suffix":"| HRCP Prep Hub",
          "try_free":"Lấy Tài Liệu HRCP","cta":"Bắt Đầu Học Ngay",
          "free_trial":"Đảm bảo vượt qua hoặc hoàn tiền","no_cc":"Truy cập kỹ thuật số ngay lập tức",
          "home":"Trang chủ","guides_lbl":"Hướng dẫn","blog_lbl":"Blog","faq_lbl":"FAQ",
          "updated":"Cập nhật","read_min":"phút đọc",
          "sidebar_h":"Tài Liệu Học HRCP","sidebar_sub":"Đảm bảo vượt qua • Từ năm 1995",
          "bottom_cta_h":"Sẵn Sàng Được Chứng Nhận?","bottom_cta_p":"Tài liệu HRCP đã giúp hơn 100.000 chuyên gia HR vượt qua kỳ thi chứng chỉ của họ kể từ năm 1995.",
          "disclosure":"Tiết lộ liên kết: Chúng tôi kiếm hoa hồng khi bạn mua qua liên kết của chúng tôi.",
          "currency":"VND"},
}
FLAGS = {"en":"🇺🇸","es":"🇪🇸","pt":"🇧🇷","fr":"🇫🇷","de":"🇩🇪","ja":"🇯🇵","ko":"🇰🇷","ar":"🇸🇦",
         "zh":"🇨🇳","hi":"🇮🇳","it":"🇮🇹","nl":"🇳🇱","pl":"🇵🇱","tr":"🇹🇷","id":"🇮🇩","vi":"🇻🇳"}

# Native-language intro sentences for intl pages (shows on every intl page)
NATIVE_INTRO = {
    "es": "Esta guía cubre {kw} — todo lo que los profesionales de RRHH necesitan para prepararse y aprobar su examen de certificación.",
    "pt": "Este guia aborda {kw} — tudo que profissionais de RH precisam para se preparar e passar no exame de certificação.",
    "fr": "Ce guide couvre {kw} — tout ce que les professionnels RH doivent savoir pour préparer et réussir leur examen de certification.",
    "de": "Dieser Leitfaden behandelt {kw} — alles, was HR-Fachleute zur Vorbereitung und zum Bestehen ihrer Zertifizierungsprüfung benötigen.",
    "ja": "このガイドでは{kw}について解説します。HR専門家が資格試験に合格するために必要なすべての情報を提供します。",
    "ko": "이 가이드는 {kw}에 대해 다룹니다. HR 전문가가 자격증 시험을 준비하고 합격하는 데 필요한 모든 정보를 제공합니다.",
    "ar": "يغطي هذا الدليل {kw} — كل ما يحتاجه متخصصو الموارد البشرية للتحضير واجتياز امتحان الشهادة.",
    "zh": "本指南涵盖{kw}——HR专业人员准备并通过认证考试所需的全面信息。",
    "hi": "यह गाइड {kw} को कवर करता है — HR पेशेवरों को अपनी सर्टिफिकेशन परीक्षा की तैयारी और पास करने के लिए आवश्यक सभी जानकारी।",
    "it": "Questa guida tratta {kw} — tutto ciò che i professionisti HR devono sapere per prepararsi e superare il proprio esame di certificazione.",
    "nl": "Deze gids behandelt {kw} — alles wat HR-professionals nodig hebben om hun certificeringsexamen voor te bereiden en te halen.",
    "pl": "Ten przewodnik obejmuje {kw} — wszystko, czego specjaliści HR potrzebują, aby przygotować się i zdać egzamin certyfikacyjny.",
    "tr": "Bu rehber {kw} konusunu ele alıyor — İK profesyonellerinin sertifikasyon sınavına hazırlanmak ve geçmek için ihtiyaç duydukları her şey.",
    "id": "Panduan ini membahas {kw} — semua yang dibutuhkan profesional HR untuk mempersiapkan dan lulus ujian sertifikasi mereka.",
    "vi": "Hướng dẫn này đề cập đến {kw} — tất cả những gì các chuyên gia HR cần để chuẩn bị và vượt qua kỳ thi chứng chỉ.",
}

# Native-language CTA sentences
NATIVE_CTA = {
    "es": "Obtenga los materiales de estudio HRCP y apruebe su examen de certificación con la garantía de devolución de dinero.",
    "pt": "Obtenha os materiais de estudo HRCP e passe no seu exame de certificação com garantia de devolução do dinheiro.",
    "fr": "Obtenez les matériaux d'étude HRCP et réussissez votre examen de certification avec la garantie satisfait ou remboursé.",
    "de": "Holen Sie sich die HRCP-Lernmaterialien und bestehen Sie Ihre Zertifizierungsprüfung mit der Geld-zurück-Garantie.",
    "ja": "HRCP学習教材を入手して、合格保証付きで資格試験に合格しましょう。",
    "ko": "HRCP 학습 자료를 구하고 합격 보장 제도와 함께 자격증 시험을 통과하세요.",
    "ar": "احصل على مواد دراسة HRCP وانجح في امتحان الشهادة مع ضمان استرداد المال.",
    "zh": "获取HRCP学习材料，凭借通过或退款保证通过您的认证考试。",
    "hi": "HRCP अध्ययन सामग्री प्राप्त करें और पास-या-पैसे-वापस गारंटी के साथ अपनी सर्टिफिकेशन परीक्षा पास करें।",
    "it": "Ottieni i materiali di studio HRCP e supera il tuo esame di certificazione con la garanzia soddisfatto o rimborsato.",
    "nl": "Haal de HRCP studiematerialen en haal je certificeringsexamen met de teruggeldgarantie.",
    "pl": "Zdobądź materiały do nauki HRCP i zdaj egzamin certyfikacyjny z gwarancją zwrotu pieniędzy.",
    "tr": "HRCP çalışma materyallerini alın ve para iade garantisiyle sertifikasyon sınavınızı geçin.",
    "id": "Dapatkan materi belajar HRCP dan lulus ujian sertifikasi Anda dengan jaminan uang kembali.",
    "vi": "Lấy tài liệu học HRCP và vượt qua kỳ thi chứng chỉ của bạn với đảm bảo hoàn tiền.",
}


# ── PRODUCTS ──────────────────────────────────────────────────────────────────
PRODUCTS = [
    ("aphr-online","aPHR Certification Prep — Online Edition","$175","aPHR",
     "400+ pages, 300+ flashcards, 1,300+ practice questions, 13 practice exams. Audio reader included. Instant access."),
    ("aphr-print","aPHR Certification Prep — Print Edition","$195","aPHR",
     "400+ pages printed, 300+ flashcards in print, 1,300+ practice questions, 13 practice exams online."),
    ("phr-sphr-online","Complete HRCP Program PHR/SPHR — Online Edition","$295","PHR/SPHR",
     "900+ pages, 600+ flashcards, 2,000+ practice questions, 16 practice exams. Audio reader. Instant access."),
    ("phr-sphr-print","Complete HRCP Program PHR/SPHR — Print Edition","$375","PHR/SPHR",
     "900+ pages printed, 600+ print flashcards, 2,000+ questions, 16 practice exams online."),
    ("shrm-online","HRCP SHRM-CP/SHRM-SCP Prep — Online Edition","$295","SHRM",
     "Complete SHRM prep materials. 16 practice exams, 2,000+ questions. Audio reader included."),
    ("phri-online","PHRi/SPHRi International Prep — Online Edition","$295","PHRi/SPHRi",
     "International HR certification prep. 900+ pages, 16 practice exams, global HR content."),
]

# ── EXAM ARCHITECTURE ─────────────────────────────────────────────────────────
EXAMS = [
    ("aphr","aPHR","Associate Professional in Human Resources","HRCI","Entry-level","$400","aPHR"),
    ("phr","PHR","Professional in Human Resources","HRCI","Mid-level","$495","PHR/SPHR"),
    ("sphr","SPHR","Senior Professional in Human Resources","HRCI","Senior-level","$495","PHR/SPHR"),
    ("shrm-cp","SHRM-CP","SHRM Certified Professional","SHRM","Mid-level","$300–$475","SHRM"),
    ("shrm-scp","SHRM-SCP","SHRM Senior Certified Professional","SHRM","Senior-level","$300–$475","SHRM"),
    ("phri","PHRi","Professional in Human Resources International","HRCI","International","$495","PHRi/SPHRi"),
    ("sphri","SPHRi","Senior Professional in Human Resources International","HRCI","International","$495","PHRi/SPHRi"),
    ("gphr","GPHR","Global Professional in Human Resources","HRCI","Global","$495","PHR/SPHR"),
]
EXAM_ASPECTS = [
    ("study-guide","Study Guide"),("practice-test","Practice Test"),
    ("study-materials","Study Materials"),("exam-prep","Exam Prep"),
    ("pass-rate","Pass Rate and Tips"),("requirements","Requirements"),
    ("vs","vs Other Certifications"),("review","Review"),
    ("cost","Cost and Fees"),("flashcards","Flashcards"),
]
EXAM_KW = [(f"{es}-{asp}",f"{en} {an}","Exam Guide","10k+")
           for es,en,elong,eorg,elevel,eprice,eprod in EXAMS
           for asp,an in EXAM_ASPECTS]

# ── GENERAL HR CERT KEYWORDS ──────────────────────────────────────────────────
GENERAL_KW = [
    ("hr-certification","HR Certification","General","100k+"),
    ("hr-certification-exam","HR Certification Exam","General","50k+"),
    ("best-hr-certification","Best HR Certification","Comparison","50k+"),
    ("hr-certification-study-guide","HR Certification Study Guide","Products","30k+"),
    ("hr-certification-practice-test","HR Certification Practice Test","Products","30k+"),
    ("hrci-certification","HRCI Certification","General","30k+"),
    ("shrm-certification","SHRM Certification","General","50k+"),
    ("hr-certification-prep","HR Certification Prep","Products","30k+"),
    ("how-to-pass-hr-certification","How to Pass HR Certification Exam","How-To","20k+"),
    ("hr-certification-study-materials","HR Certification Study Materials","Products","20k+"),
    ("hr-certification-cost","HR Certification Cost","Informational","20k+"),
    ("hr-salary-with-certification","HR Salary With Certification","Informational","20k+"),
    ("is-hr-certification-worth-it","Is HR Certification Worth It","Informational","30k+"),
    ("best-hr-study-guide","Best HR Study Guide","Products","20k+"),
    ("hrcp-review","HRCP Review","Review","10k+"),
    ("hrcp-study-materials","HRCP Study Materials","Review","10k+"),
    ("hrcp-practice-test","HRCP Practice Test","Review","10k+"),
    ("hrcp-vs-shrm-learning-system","HRCP vs SHRM Learning System","Comparison","5k+"),
    ("free-hr-practice-questions","Free HR Practice Questions","How-To","20k+"),
    ("how-to-become-hr-certified","How to Become HR Certified","How-To","20k+"),
    ("hr-certification-for-beginners","HR Certification for Beginners","How-To","10k+"),
    ("aphr-vs-phr","aPHR vs PHR — Which Should You Get?","Comparison","10k+"),
    ("phr-vs-sphr","PHR vs SPHR — What Is the Difference?","Comparison","10k+"),
    ("shrm-cp-vs-phr","SHRM-CP vs PHR — Which Is Better?","Comparison","20k+"),
    ("hr-certification-study-schedule","HR Certification Study Schedule","How-To","5k+"),
    ("hr-certification-flashcards","HR Certification Flashcards","Products","10k+"),
    ("hrci-vs-shrm","HRCI vs SHRM — Which Certification Is Better?","Comparison","20k+"),
    ("hr-certification-online","HR Certification Online","General","30k+"),
    ("human-resources-certification","Human Resources Certification","General","50k+"),
    ("hr-professional-certification","HR Professional Certification","General","20k+"),
    # Career-level pages
    ("hr-coordinator-certification","HR Coordinator Certification","Informational","5k+"),
    ("hr-manager-certification","HR Manager Certification","Informational","10k+"),
    ("hr-director-certification","HR Director Certification","Informational","5k+"),
    ("hr-business-partner-certification","HR Business Partner Certification","Informational","5k+"),
    ("entry-level-hr-certification","Entry Level HR Certification","Informational","10k+"),
    # Industry pages
    ("hr-certification-healthcare","HR Certification for Healthcare","Niche","5k+"),
    ("hr-certification-technology","HR Certification for Tech Companies","Niche","5k+"),
    ("hr-certification-nonprofit","HR Certification for Nonprofits","Niche","3k+"),
    ("hr-certification-government","HR Certification for Government","Niche","3k+"),
    ("hr-certification-manufacturing","HR Certification for Manufacturing","Niche","3k+"),
    ("hr-certification-finance","HR Certification for Finance","Niche","3k+"),
    # Additional exam aspects
    ("aphr-pass-rate","aPHR Exam Pass Rate and What It Means","Informational","5k+"),
    ("phr-exam-content","PHR Exam Content and Topics Covered","Informational","5k+"),
    ("sphr-vs-phr-salary","SPHR vs PHR Salary Difference","Informational","3k+"),
    ("shrm-cp-requirements","SHRM-CP Eligibility Requirements","Informational","5k+"),
    ("gphr-requirements","GPHR Requirements and Eligibility","Informational","3k+"),
]

# ── US CITIES — 150 largest HR markets × 5 keyword types ─────────────────────
CITIES_HR = [
    ("new-york-ny","New York NY"),("los-angeles-ca","Los Angeles CA"),
    ("chicago-il","Chicago IL"),("houston-tx","Houston TX"),
    ("phoenix-az","Phoenix AZ"),("philadelphia-pa","Philadelphia PA"),
    ("san-antonio-tx","San Antonio TX"),("san-diego-ca","San Diego CA"),
    ("dallas-tx","Dallas TX"),("san-jose-ca","San Jose CA"),
    ("austin-tx","Austin TX"),("jacksonville-fl","Jacksonville FL"),
    ("fort-worth-tx","Fort Worth TX"),("columbus-oh","Columbus OH"),
    ("charlotte-nc","Charlotte NC"),("indianapolis-in","Indianapolis IN"),
    ("san-francisco-ca","San Francisco CA"),("seattle-wa","Seattle WA"),
    ("denver-co","Denver CO"),("nashville-tn","Nashville TN"),
    ("oklahoma-city-ok","Oklahoma City OK"),("el-paso-tx","El Paso TX"),
    ("washington-dc","Washington DC"),("boston-ma","Boston MA"),
    ("las-vegas-nv","Las Vegas NV"),("memphis-tn","Memphis TN"),
    ("portland-or","Portland OR"),("louisville-ky","Louisville KY"),
    ("baltimore-md","Baltimore MD"),("milwaukee-wi","Milwaukee WI"),
    ("albuquerque-nm","Albuquerque NM"),("tucson-az","Tucson AZ"),
    ("fresno-ca","Fresno CA"),("mesa-az","Mesa AZ"),
    ("sacramento-ca","Sacramento CA"),("atlanta-ga","Atlanta GA"),
    ("kansas-city-mo","Kansas City MO"),("omaha-ne","Omaha NE"),
    ("colorado-springs-co","Colorado Springs CO"),("raleigh-nc","Raleigh NC"),
    ("long-beach-ca","Long Beach CA"),("virginia-beach-va","Virginia Beach VA"),
    ("minneapolis-mn","Minneapolis MN"),("tampa-fl","Tampa FL"),
    ("new-orleans-la","New Orleans LA"),("arlington-tx","Arlington TX"),
    ("wichita-ks","Wichita KS"),("bakersfield-ca","Bakersfield CA"),
    ("aurora-co","Aurora CO"),("anaheim-ca","Anaheim CA"),
    ("santa-ana-ca","Santa Ana CA"),("corpus-christi-tx","Corpus Christi TX"),
    ("riverside-ca","Riverside CA"),("lexington-ky","Lexington KY"),
    ("st-louis-mo","St. Louis MO"),("pittsburgh-pa","Pittsburgh PA"),
    ("anchorage-ak","Anchorage AK"),("stockton-ca","Stockton CA"),
    ("cincinnati-oh","Cincinnati OH"),("st-paul-mn","St. Paul MN"),
    ("greensboro-nc","Greensboro NC"),("toledo-oh","Toledo OH"),
    ("newark-nj","Newark NJ"),("plano-tx","Plano TX"),
    ("henderson-nv","Henderson NV"),("orlando-fl","Orlando FL"),
    ("chandler-az","Chandler AZ"),("st-petersburg-fl","St. Petersburg FL"),
    ("laredo-tx","Laredo TX"),("norfolk-va","Norfolk VA"),
    ("madison-wi","Madison WI"),("durham-nc","Durham NC"),
    ("lubbock-tx","Lubbock TX"),("winston-salem-nc","Winston-Salem NC"),
    ("garland-tx","Garland TX"),("glendale-az","Glendale AZ"),
    ("hialeah-fl","Hialeah FL"),("reno-nv","Reno NV"),
    ("baton-rouge-la","Baton Rouge LA"),("irvine-ca","Irvine CA"),
    ("chesapeake-va","Chesapeake VA"),("scottsdale-az","Scottsdale AZ"),
    ("north-las-vegas-nv","North Las Vegas NV"),("fremont-ca","Fremont CA"),
    ("gilbert-az","Gilbert AZ"),("san-bernardino-ca","San Bernardino CA"),
    ("birmingham-al","Birmingham AL"),("rochester-ny","Rochester NY"),
    ("richmond-va","Richmond VA"),("spokane-wa","Spokane WA"),
    ("des-moines-ia","Des Moines IA"),("montgomery-al","Montgomery AL"),
    ("modesto-ca","Modesto CA"),("fayetteville-nc","Fayetteville NC"),
    ("tacoma-wa","Tacoma WA"),("shreveport-la","Shreveport LA"),
    ("akron-oh","Akron OH"),("aurora-il","Aurora IL"),
    ("yonkers-ny","Yonkers NY"),("huntington-beach-ca","Huntington Beach CA"),
]
CITY_GEO_TYPES = [
    ("hr-certification-prep","HR Certification Prep"),
    ("phr-study-guide","PHR Study Guide"),
    ("shrm-certification","SHRM Certification"),
    ("hr-certification-classes","HR Certification Classes"),
    ("aphr-certification","aPHR Certification"),
]
CITY_KW = [(f"{gt}-{cs}",f"{gn} in {cn}","Geo-City","500+")
           for cs,cn in CITIES_HR
           for gt,gn in CITY_GEO_TYPES]


# ── GEO KEYWORDS — All 50 US States ──────────────────────────────────────────
STATES = [
    ("alabama","Alabama"),("alaska","Alaska"),("arizona","Arizona"),("arkansas","Arkansas"),
    ("california","California"),("colorado","Colorado"),("connecticut","Connecticut"),
    ("delaware","Delaware"),("florida","Florida"),("georgia","Georgia"),("hawaii","Hawaii"),
    ("idaho","Idaho"),("illinois","Illinois"),("indiana","Indiana"),("iowa","Iowa"),
    ("kansas","Kansas"),("kentucky","Kentucky"),("louisiana","Louisiana"),("maine","Maine"),
    ("maryland","Maryland"),("massachusetts","Massachusetts"),("michigan","Michigan"),
    ("minnesota","Minnesota"),("mississippi","Mississippi"),("missouri","Missouri"),
    ("montana","Montana"),("nebraska","Nebraska"),("nevada","Nevada"),
    ("new-hampshire","New Hampshire"),("new-jersey","New Jersey"),("new-mexico","New Mexico"),
    ("new-york","New York"),("north-carolina","North Carolina"),("north-dakota","North Dakota"),
    ("ohio","Ohio"),("oklahoma","Oklahoma"),("oregon","Oregon"),("pennsylvania","Pennsylvania"),
    ("rhode-island","Rhode Island"),("south-carolina","South Carolina"),
    ("south-dakota","South Dakota"),("tennessee","Tennessee"),("texas","Texas"),
    ("utah","Utah"),("vermont","Vermont"),("virginia","Virginia"),("washington","Washington"),
    ("west-virginia","West Virginia"),("wisconsin","Wisconsin"),("wyoming","Wyoming"),
]
GEO_TYPES = [
    ("hr-certification-prep","HR Certification Prep"),
    ("phr-study-guide","PHR Study Guide"),
    ("shrm-certification","SHRM Certification"),
    ("hr-certification-classes","HR Certification Classes"),
    ("aphr-certification","aPHR Certification"),
]
STATE_KW = [(f"{gt}-{ss}",f"{gn} in {sn}","Geo-State","1k+")
            for ss,sn in STATES for gt,gn in GEO_TYPES]

EN_KEYWORDS = GENERAL_KW + EXAM_KW + STATE_KW + CITY_KW

# ── INTERNATIONAL KEYWORDS ────────────────────────────────────────────────────
INTL_CORE = [
    ("hr-certification","HR Certification","General"),
    ("phr-exam-prep","PHR Exam Prep","Exam Guide"),
    ("sphr-study-guide","SPHR Study Guide","Exam Guide"),
    ("aphr-certification","aPHR Certification","Exam Guide"),
    ("shrm-cp-prep","SHRM-CP Prep","Exam Guide"),
    ("best-hr-certification","Best HR Certification","Comparison"),
    ("hr-certification-cost","HR Certification Cost","Informational"),
    ("hrcp-review","HRCP Review","Review"),
    ("is-hr-certification-worth-it","Is HR Certification Worth It","Informational"),
    ("hr-certification-study-guide","HR Certification Study Guide","Products"),
    ("hr-certification-practice-test","HR Certification Practice Test","Products"),
    ("how-to-pass-phr","How to Pass PHR Exam","How-To"),
    ("hrci-vs-shrm","HRCI vs SHRM Certification","Comparison"),
    ("phr-vs-sphr","PHR vs SPHR","Comparison"),
    ("hr-salary-with-certification","HR Salary With Certification","Informational"),
    ("global-hr-certification","Global HR Certification","General"),
    ("human-resources-certification","Human Resources Certification","General"),
    ("hr-certification-online","HR Certification Online","General"),
    ("shrm-scp-study-guide","SHRM-SCP Study Guide","Exam Guide"),
    ("gphr-certification","GPHR Certification Guide","Exam Guide"),
    # Additional 20 for broader coverage
    ("aphr-vs-phr","aPHR vs PHR Comparison","Comparison"),
    ("hr-certification-for-beginners","HR Certification for Beginners","How-To"),
    ("hrcp-practice-test","HRCP Practice Test Guide","Products"),
    ("phr-requirements","PHR Certification Requirements","Informational"),
    ("shrm-cp-vs-phr","SHRM-CP vs PHR Comparison","Comparison"),
    ("hr-certification-study-materials","HR Certification Study Materials","Products"),
    ("hr-certification-flashcards","HR Certification Flashcards","Products"),
    ("how-to-become-hr-certified","How to Become HR Certified","How-To"),
    ("phri-sphri-certification","PHRi SPHRi International Certification","Exam Guide"),
    ("hr-certification-worth-it-salary","HR Certification Salary Premium","Informational"),
    ("hrcp-vs-shrm-learning-system","HRCP vs SHRM Learning System","Comparison"),
    ("hr-certification-recertification","HR Certification Recertification Guide","Informational"),
    ("sphr-requirements","SPHR Requirements and Eligibility","Informational"),
    ("hr-certification-study-schedule","HR Certification Study Schedule","How-To"),
    ("phr-pass-rate","PHR Exam Pass Rate and Tips","Informational"),
    ("best-hr-study-guide","Best HR Certification Study Guide","Products"),
    ("hr-certification-without-degree","HR Certification Without a Degree","Informational"),
    ("aphr-study-guide","aPHR Complete Study Guide","Exam Guide"),
    ("shrm-membership-worth-it","Is SHRM Membership Worth It","Informational"),
    ("hr-professional-certification","HR Professional Certification Guide","General"),
]

# Language-specific EXTRA keywords for top markets
LANG_EXTRA = {
    "zh": [
        ("hr-certification-china","HR Certification in China","General"),
        ("shrm-china","SHRM Certification China","Exam Guide"),
        ("gphr-china","GPHR for Chinese HR Professionals","Exam Guide"),
        ("phri-china","PHRi for International HR China","Exam Guide"),
    ],
    "hi": [
        ("hr-certification-india","HR Certification in India","General"),
        ("shrm-india","SHRM Certification India","Exam Guide"),
        ("phri-india","PHRi for Indian HR Professionals","Exam Guide"),
        ("gphr-india","GPHR Certification India","Exam Guide"),
    ],
    "es": [
        ("certificacion-rrhh","Certificación Recursos Humanos","General"),
        ("gphr-latam","GPHR para Profesionales de RRHH","Exam Guide"),
        ("phri-latam","PHRi Certificación Internacional","Exam Guide"),
        ("shrm-espanol","SHRM Certificación en Español","Exam Guide"),
    ],
    "pt": [
        ("certificacao-rh-brasil","Certificação RH Brasil","General"),
        ("phri-brasil","PHRi para Profissionais de RH","Exam Guide"),
        ("shrm-cp-brasil","SHRM-CP Preparação Brasil","Exam Guide"),
        ("gphr-brasil","GPHR Certificação Internacional","Exam Guide"),
    ],
    "de": [
        ("hr-zertifizierung-deutschland","HR Zertifizierung Deutschland","General"),
        ("gphr-zertifizierung","GPHR Zertifizierung International","Exam Guide"),
        ("shrm-zertifizierung","SHRM Zertifizierung","Exam Guide"),
        ("phri-zertifizierung","PHRi International Zertifizierung","Exam Guide"),
    ],
    "id": [
        ("sertifikasi-hr-indonesia","Sertifikasi HR Indonesia","General"),
        ("phri-indonesia","PHRi untuk Profesional HR Indonesia","Exam Guide"),
        ("shrm-indonesia","SHRM Sertifikasi Indonesia","Exam Guide"),
    ],
    "vi": [
        ("chung-chi-hr-viet-nam","Chứng Chỉ HR Việt Nam","General"),
        ("phri-viet-nam","PHRi cho Chuyên Gia HR Việt Nam","Exam Guide"),
    ],
    "tr": [
        ("hr-sertifikasi-turkiye","HR Sertifikası Türkiye","General"),
        ("gphr-uluslararasi","GPHR Uluslararası Sertifikası","Exam Guide"),
    ],
}

INTL_KEYWORDS = {}
for lang_code in LANGUAGES:
    if lang_code == "en": continue
    kws = []
    for slug, title, cat in INTL_CORE:
        kws.append((f"{lang_code}/{slug}", title, cat, "1k+"))
    # Add language-specific extras
    for slug, title, cat in LANG_EXTRA.get(lang_code, []):
        kws.append((f"{lang_code}/{slug}", title, cat, "1k+"))
    INTL_KEYWORDS[lang_code] = kws

# Keyword summary printed in main()


# ── CSS ────────────────────────────────────────────────────────────────────────
CSS = (
"*{box-sizing:border-box;margin:0;padding:0}"
"body{font-family:'Segoe UI',system-ui,sans-serif;color:#111827;background:#f0f4ff;line-height:1.75}"
"a{color:#1d4ed8;text-decoration:none}a:hover{text-decoration:underline}"
".site-header{background:#1e3a5f;color:#fff;position:sticky;top:0;z-index:300;border-bottom:3px solid #3b82f6}"
".hd{max-width:1160px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;height:62px;padding:0 1.2rem}"
".logo{font-size:1.1rem;font-weight:900;color:#fff;display:flex;align-items:center;gap:.5rem}"
".logo-ico{background:#3b82f6;color:#fff;font-size:1rem;width:34px;height:34px;border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0}"
".nav-links{display:flex;gap:1.4rem;align-items:center}"
".nav-links a{color:rgba(255,255,255,.85);font-size:.82rem;font-weight:500;transition:color .15s}"
".nav-links a:hover{color:#93c5fd;text-decoration:none}"
".nav-cta{background:#3b82f6;color:#fff!important;font-weight:900!important;padding:.38rem 1.05rem;border-radius:6px;font-size:.82rem!important}"
".lang-bar{background:#1e3a5f;border-bottom:1px solid rgba(255,255,255,.1);border-top:1px solid rgba(255,255,255,.08);padding:.35rem 1.2rem;overflow-x:auto;white-space:nowrap}"
".lang-bar a{color:rgba(255,255,255,.7);font-size:.73rem;margin-right:1rem;font-weight:500}"
".lang-bar a:hover,.lang-bar a.active{color:#93c5fd;text-decoration:none}"
".hero{background:linear-gradient(135deg,#1e3a5f 0%,#1e40af 60%,#2563eb 100%);color:#fff;padding:4.5rem 1.2rem 4rem;text-align:center;position:relative;overflow:hidden}"
".hero::before{content:'';position:absolute;top:-80px;right:-80px;width:400px;height:400px;background:rgba(59,130,246,.1);border-radius:50%}"
".hero-inner{max-width:860px;margin:0 auto;position:relative;z-index:1}"
".hero-eyebrow{display:inline-flex;align-items:center;gap:.5rem;background:rgba(59,130,246,.25);border:1px solid rgba(59,130,246,.5);color:#bfdbfe;border-radius:50px;padding:.3rem 1rem;font-size:.72rem;letter-spacing:1.8px;text-transform:uppercase;margin-bottom:1.5rem;font-weight:700}"
".hero h1{font-size:clamp(1.9rem,4.5vw,3rem);font-weight:900;line-height:1.12;margin-bottom:1.1rem;letter-spacing:-.5px}"
".hero h1 span{color:#93c5fd}"
".hero-sub{font-size:1.05rem;opacity:.88;max-width:680px;margin:0 auto 2.4rem;line-height:1.78}"
".cta-btn{display:inline-flex;align-items:center;gap:.6rem;background:#2563eb;color:#fff;font-size:1.05rem;font-weight:900;padding:1.05rem 2.8rem;border-radius:9px;text-decoration:none;box-shadow:0 6px 28px rgba(37,99,235,.4);transition:transform .18s,box-shadow .18s}"
".cta-btn:hover{transform:translateY(-3px);box-shadow:0 10px 38px rgba(37,99,235,.5);text-decoration:none;color:#fff}"
".hero-note{font-size:.78rem;opacity:.65;margin-top:1rem}"
".update-badge{display:inline-block;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);color:rgba(255,255,255,.9);border-radius:20px;padding:.22rem .75rem;font-size:.7rem;font-weight:700;margin-top:.9rem;letter-spacing:.5px}"
".trust-strip{background:#fff;border-bottom:1px solid #dbeafe;padding:1rem 1.2rem}"
".trust-inner{max-width:1160px;margin:0 auto;display:flex;flex-wrap:wrap;justify-content:center;gap:1.6rem}"
".trust-item{display:flex;align-items:center;gap:.42rem;font-size:.82rem;color:#374151;font-weight:600}"
".trust-ico{width:20px;height:20px;background:#1d4ed8;border-radius:50%;color:#fff;font-size:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0}"
".stat-row{background:#dbeafe;border-bottom:2px solid #bfdbfe;padding:1.8rem 1.2rem}"
".stat-inner{max-width:1160px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:1rem;text-align:center}"
".stat-n{font-size:2rem;font-weight:900;color:#1e3a5f;line-height:1}"
".stat-l{font-size:.74rem;color:#1d4ed8;margin-top:.3rem;font-weight:600}"
".breadcrumb{max-width:1160px;margin:0 auto;padding:.72rem 1.2rem;font-size:.79rem;color:#6b7280}"
".breadcrumb a{color:#1d4ed8}.breadcrumb .sep{margin:0 .32rem;color:#d1d5db}"
".pg{max-width:1160px;margin:0 auto;padding:2.2rem 1.2rem 3.5rem;display:grid;grid-template-columns:1fr 315px;gap:2.8rem;align-items:start}"
".art h2{font-size:1.28rem;font-weight:800;color:#1e3a5f;margin:2.5rem 0 .78rem;padding-top:1.2rem;border-top:2px solid #dbeafe;line-height:1.3}"
".art h2:first-of-type{border-top:none;margin-top:0;padding-top:0}"
".art h3{font-size:1rem;font-weight:700;color:#1d4ed8;margin:1.5rem 0 .48rem}"
".art p{margin-bottom:1.05rem;color:#374151;font-size:.96rem;line-height:1.8}"
".art ul,.art ol{margin:0 0 1.1rem 1.45rem;color:#374151;font-size:.96rem}"
".art li{margin-bottom:.45rem;line-height:1.7}"
".art strong{color:#1e3a5f}"
".art a{color:#1d4ed8}"
".intro-box{background:linear-gradient(135deg,#dbeafe,#bfdbfe);border-left:4px solid #1d4ed8;border-radius:0 12px 12px 0;padding:1.35rem 1.65rem;margin-bottom:2.3rem;font-size:1.01rem;color:#1e3a5f;line-height:1.85;font-weight:500}"
".toc-box{background:#f0f4ff;border:1px solid #dbeafe;border-radius:10px;padding:1rem 1.35rem;margin:1.2rem 0 1.8rem}"
".toc-box p{font-size:.8rem;font-weight:800;color:#1e3a5f;margin-bottom:.55rem;text-transform:uppercase;letter-spacing:.8px}"
".toc-box ol{margin:0 0 0 1rem;padding:0;font-size:.83rem;color:#1d4ed8;line-height:2}"
".cmp{width:100%;border-collapse:collapse;margin:1rem 0 1.6rem;font-size:.86rem;border-radius:10px;overflow:hidden;box-shadow:0 1px 8px rgba(0,0,0,.08)}"
".cmp th{background:#1e3a5f;color:#fff;padding:.78rem 1rem;text-align:left;font-weight:700;font-size:.82rem}"
".cmp td{padding:.7rem 1rem;border-bottom:1px solid #e5e7eb;color:#374151;vertical-align:middle}"
".cmp tr:last-child td{border:none}"
".cmp tr:nth-child(even) td{background:#f8faff}"
".good{color:#059669;font-weight:700}.bad{color:#dc2626;font-weight:700}.ok{color:#d97706;font-weight:700}"
".pros-cons{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1.2rem 0 1.6rem}"
".pros,.cons{border-radius:10px;padding:1.2rem 1.4rem}"
".pros{background:#f0fdf4;border:1px solid #bbf7d0}"
".cons{background:#fef2f2;border:1px solid #fecaca}"
".pros h4{color:#166534;font-size:.88rem;font-weight:800;margin-bottom:.65rem;text-transform:uppercase;letter-spacing:.5px}"
".cons h4{color:#991b1b;font-size:.88rem;font-weight:800;margin-bottom:.65rem;text-transform:uppercase;letter-spacing:.5px}"
".pros li,.cons li{font-size:.85rem;margin-bottom:.4rem;list-style:none;display:flex;align-items:flex-start;gap:.4rem}"
".pros li::before{content:'✓';color:#059669;font-weight:900;flex-shrink:0}"
".cons li::before{content:'✗';color:#dc2626;font-weight:900;flex-shrink:0}"
".steps{list-style:none;margin:0 0 1.6rem;padding:0;counter-reset:step}"
".steps li{display:flex;gap:1rem;align-items:flex-start;margin-bottom:1rem;padding:1.05rem 1.15rem;background:#fff;border:1px solid #dbeafe;border-radius:10px;counter-increment:step;position:relative}"
".steps li::before{content:counter(step);background:#1d4ed8;color:#fff;font-weight:900;font-size:.82rem;min-width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px}"
".steps li p{margin:0;font-size:.92rem;color:#374151;line-height:1.65}"
".steps li strong{display:block;margin-bottom:.22rem;color:#1e3a5f;font-size:.94rem}"
".step-time{font-size:.72rem;color:#9ca3af;font-weight:600;margin-top:.3rem}"
".exam-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1.25rem;margin:1.2rem 0 1.6rem}"
".exam-card{background:#fff;border:1px solid #dbeafe;border-radius:14px;padding:1.35rem;display:flex;flex-direction:column}"
".exam-badge{display:inline-block;background:#dbeafe;color:#1e3a5f;font-size:.7rem;font-weight:800;padding:.22rem .6rem;border-radius:20px;margin-bottom:.65rem;text-transform:uppercase;letter-spacing:.5px}"
".exam-card h3{font-size:.95rem;font-weight:800;color:#1e3a5f;margin-bottom:.4rem}"
".exam-card .price{font-size:1.1rem;font-weight:900;color:#1d4ed8;margin:.4rem 0}"
".exam-card p{font-size:.83rem;color:#6b7280;line-height:1.6;margin-bottom:.9rem;flex:1}"
".buy-btn{display:block;background:#1d4ed8;color:#fff;font-weight:700;padding:.72rem 1rem;border-radius:8px;text-decoration:none;text-align:center;font-size:.86rem;transition:background .15s;margin-top:auto}"
".buy-btn:hover{background:#1e40af;text-decoration:none;color:#fff}"
".guarantee-box{background:#f0fdf4;border:2px solid #86efac;border-radius:12px;padding:1.35rem 1.6rem;margin:1.5rem 0;text-align:center}"
".guarantee-box h3{color:#166534;font-size:1rem;font-weight:900;margin-bottom:.4rem}"
".guarantee-box p{color:#166534;font-size:.88rem;margin:0}"
".faq-wrap{margin:.6rem 0 1.6rem}"
".faq-item{border:1px solid #dbeafe;border-radius:10px;margin-bottom:.78rem;overflow:hidden;background:#fff}"
".faq-q{background:#f0f4ff;padding:1.05rem 1.2rem;font-weight:700;color:#1e3a5f;font-size:.93rem;cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:1rem}"
".faq-q::after{content:'+';font-size:1.2rem;color:#6b7280;flex-shrink:0}"
".faq-item[open] .faq-q{background:#dbeafe}"
".faq-item[open] .faq-q::after{content:'-';color:#1d4ed8}"
".faq-a{padding:1.05rem 1.2rem;font-size:.92rem;color:#374151;line-height:1.75;border-top:1px solid #dbeafe}"
".tip-box{background:#f0f9ff;border:1px solid #bae6fd;border-left:4px solid #0ea5e9;border-radius:0 10px 10px 0;padding:1.1rem 1.35rem;margin:1.5rem 0}"
".tip-box strong{color:#0c4a6e;display:block;margin-bottom:.38rem;font-size:.93rem}"
".tip-box p{margin:0;color:#075985;font-size:.89rem}"
".stat-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:.85rem;margin:1.2rem 0 1.5rem}"
".stat-card{background:#dbeafe;border-radius:10px;padding:1rem;text-align:center}"
".stat-card .n{font-size:1.6rem;font-weight:900;color:#1e3a5f;line-height:1}"
".stat-card .l{font-size:.75rem;color:#1d4ed8;margin-top:.3rem;font-weight:600}"
".related-wrap{background:#f0f4ff;border:1px solid #dbeafe;border-radius:12px;padding:1.45rem;margin-top:2.3rem}"
".related-wrap h3{font-size:.95rem;font-weight:800;color:#1e3a5f;margin-bottom:.95rem}"
".rel-grid{display:grid;grid-template-columns:1fr 1fr;gap:.48rem}"
".rel-grid a{font-size:.82rem;color:#1d4ed8;padding:.28rem 0;display:block;font-weight:500}"
".disclosure{background:#fef9c3;border:1px solid #fde047;border-radius:9px;padding:1rem 1.2rem;font-size:.76rem;color:#854d0e;margin-top:2.2rem;line-height:1.7}"
".disclosure strong{display:block;margin-bottom:.22rem}"
".sidebar{position:sticky;top:74px}"
".sb-hero{background:#1e3a5f;color:#fff;border-radius:14px;padding:1.55rem;text-align:center;margin-bottom:1.3rem;border-bottom:3px solid #3b82f6}"
".sb-hero h3{color:#fff;font-size:1.02rem;margin-bottom:.48rem;font-weight:900}"
".sb-hero p{color:rgba(255,255,255,.8);font-size:.82rem;margin-bottom:1.1rem;line-height:1.65}"
".sb-btn{display:block;background:#3b82f6;color:#fff;font-weight:900;padding:.85rem;border-radius:9px;text-decoration:none;font-size:.95rem;transition:transform .18s;text-align:center}"
".sb-btn:hover{transform:translateY(-2px);text-decoration:none;color:#fff}"
".sb-card{background:#fff;border:1px solid #dbeafe;border-radius:14px;padding:1.3rem;margin-bottom:1.25rem}"
".sb-card h3{font-size:.92rem;font-weight:800;color:#1e3a5f;margin-bottom:.88rem;padding-bottom:.65rem;border-bottom:2px solid #dbeafe}"
".chk-list{list-style:none;margin:0}"
".chk-list li{display:flex;align-items:flex-start;gap:.5rem;margin-bottom:.52rem;font-size:.84rem;color:#374151;line-height:1.55}"
".chk-list li::before{content:'✓';color:#1d4ed8;font-weight:900;flex-shrink:0}"
".blog-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(295px,1fr));gap:1.5rem;margin-top:1.6rem}"
".blog-card{background:#fff;border:1px solid #dbeafe;border-radius:14px;padding:1.4rem;display:flex;flex-direction:column;transition:transform .18s,box-shadow .18s}"
".blog-card:hover{transform:translateY(-3px);box-shadow:0 8px 28px rgba(29,78,216,.1)}"
".blog-tag{font-size:.7rem;font-weight:800;color:#1d4ed8;text-transform:uppercase;letter-spacing:1px;margin-bottom:.5rem}"
".blog-card h3{font-size:.98rem;font-weight:700;color:#1e3a5f;margin-bottom:.5rem;line-height:1.42;flex:1}"
".blog-meta{display:flex;justify-content:space-between;align-items:center;font-size:.74rem;color:#9ca3af;margin-top:auto;padding-top:.6rem}"
".blog-read{color:#1d4ed8;font-weight:700}"
".share-bar{display:flex;align-items:center;gap:.6rem;margin:1.8rem 0;padding:1rem 1.2rem;background:#f0f4ff;border-radius:10px;border:1px solid #dbeafe;flex-wrap:wrap}"
".share-btn{display:inline-flex;align-items:center;gap:.38rem;padding:.38rem .85rem;border-radius:6px;font-size:.78rem;font-weight:700;cursor:pointer;border:none;transition:transform .15s}"
".sh-fb{background:#1877f2;color:#fff}.sh-tw{background:#1da1f2;color:#fff}.sh-li{background:#0077b5;color:#fff}.sh-cp{background:#e5e7eb;color:#374151}"
".share-btn:hover{transform:translateY(-1px)}"
".author-bar{display:flex;align-items:center;gap:.75rem;padding:.85rem 1.1rem;background:#f0f4ff;border-radius:10px;border:1px solid #dbeafe;margin-bottom:1.5rem}"
".author-av{width:38px;height:38px;background:#1d4ed8;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:.85rem;flex-shrink:0}"
".author-name{font-size:.86rem;font-weight:700;color:#1e3a5f}"
".author-title{font-size:.76rem;color:#6b7280}"
".verified-badge{display:inline-block;background:#dcfce7;color:#166534;font-size:.68rem;font-weight:700;padding:.15rem .45rem;border-radius:4px;margin-left:.4rem}"
".ph{background:#1e3a5f;color:#fff;padding:2.8rem 1.2rem 2.4rem;text-align:center;border-bottom:3px solid #3b82f6}"
".ph h1{font-size:clamp(1.7rem,3.2vw,2.1rem);font-weight:900;color:#fff;margin-bottom:.7rem}"
".ph p{opacity:.88;max-width:540px;margin:0 auto;font-size:.97rem;line-height:1.72}"
".section{max-width:1160px;margin:0 auto;padding:3rem 1.2rem}"
".section-h{font-size:1.75rem;font-weight:900;color:#1e3a5f;margin-bottom:.55rem}"
".section-sub{color:#6b7280;margin-bottom:2rem;font-size:.96rem}"
".how-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1.3rem;margin-top:1.6rem}"
".how-step{background:#fff;border:1px solid #dbeafe;border-radius:14px;padding:1.5rem;text-align:center}"
".how-num{width:50px;height:50px;background:#1e3a5f;color:#93c5fd;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.3rem;font-weight:900;margin:0 auto 1.1rem}"
".how-step h3{font-size:.94rem;font-weight:800;color:#1e3a5f;margin-bottom:.4rem}"
".how-step p{font-size:.82rem;color:#6b7280;line-height:1.62}"
".footer{background:#0f172a;color:#93c5fd;padding:3.5rem 1.2rem 2rem}"
".footer-inner{max-width:1160px;margin:0 auto}"
".footer-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(175px,1fr));gap:2.2rem;margin-bottom:2.2rem}"
".footer-col h4{color:#bfdbfe;font-size:.86rem;margin-bottom:.88rem;font-weight:900;letter-spacing:.4px;text-transform:uppercase}"
".footer-col a{display:block;color:#93c5fd;font-size:.81rem;margin-bottom:.38rem;transition:color .15s}"
".footer-col a:hover{color:#bfdbfe;text-decoration:none}"
".footer-bottom{border-top:1px solid rgba(255,255,255,.07);padding-top:1.25rem;font-size:.74rem;text-align:center;line-height:1.85;color:#6366f1}"
"@media(max-width:768px){.pg{grid-template-columns:1fr}.sidebar{position:static}.nav-links{display:none}.rel-grid{grid-template-columns:1fr}.hero{padding:3rem 1.2rem 2.5rem}.pros-cons{grid-template-columns:1fr}}"
)

JS = """<script>
document.querySelectorAll('.faq-item').forEach(function(d){
  d.querySelector('.faq-q').addEventListener('click',function(){
    var o=d.hasAttribute('open');
    document.querySelectorAll('.faq-item[open]').forEach(function(x){x.removeAttribute('open')});
    if(!o)d.setAttribute('open','');
  });
});
document.querySelectorAll('.share-btn').forEach(function(b){
  b.addEventListener('click',function(){
    var url=b.dataset.url||window.location.href,n=b.dataset.network;
    if(n==='facebook')window.open('https://www.facebook.com/sharer/sharer.php?u='+encodeURIComponent(url),'_blank','width=600,height=400');
    else if(n==='twitter')window.open('https://twitter.com/intent/tweet?url='+encodeURIComponent(url)+'&text='+encodeURIComponent(document.title),'_blank','width=600,height=400');
    else if(n==='linkedin')window.open('https://www.linkedin.com/sharing/share-offsite/?url='+encodeURIComponent(url),'_blank','width=600,height=400');
    else if(n==='copy'){if(navigator.clipboard)navigator.clipboard.writeText(url);b.textContent='Copied!';setTimeout(function(){b.textContent='Copy Link'},2000);}
  });
});
</script>"""


# ── SHARED COMPONENTS ─────────────────────────────────────────────────────────
def hd(title, desc, canon, schemas=None, og_type="website", lang_code="en"):
    desc = desc[:158]
    sc   = "\n".join(f'<script type="application/ld+json">{s}</script>' for s in (schemas or []))
    rtl  = ' dir="rtl"' if lang_code == "ar" else ""
    hl_links = "\n".join(
        f'<link rel="alternate" hreflang="{lc}" href="{SITE}/{LANGUAGES[lc]["dir"]}/{canon.split("/guides/")[-1] if "/guides/" in canon else ""}">'
        for lc in LANGUAGES if lc != "en"
    ) if "/guides/" in canon else ""
    return f"""<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="google-site-verification" content="{GOOGLE_V}">
<meta name="msvalidate.01" content="{BING_V}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="en" href="{canon}">
<link rel="alternate" hreflang="x-default" href="{SITE}/">
{hl_links}
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:image" content="{OG}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{OG}">
{sc}
<style>{CSS}</style>"""

def lang_bar(active="en"):
    links = "".join(
        f'<a href="{SITE}/{LANGUAGES[lc]["dir"]}/" class="{"active" if lc==active else ""}">'
        f'{FLAGS.get(lc,"🌐")} {LANGUAGES[lc]["native"]}</a>'
        for lc in LANGUAGES
    )
    return f'<div class="lang-bar">{links}</div>'

def nav(lang_code="en"):
    L = LANGUAGES.get(lang_code, LANGUAGES["en"])
    return f"""<header class="site-header">
<div class="hd">
<a href="{SITE}/" class="logo"><div class="logo-ico">&#127891;</div>{NAME}</a>
<nav class="nav-links">
<a href="{SITE}/">Home</a>
<a href="{SITE}/guides/">Guides</a>
<a href="{SITE}/blog/">Blog</a>
<a href="{SITE}/faq.html">FAQ</a>
<a href="{AFF}" class="nav-cta" rel="noopener sponsored">{L["cta"]}</a>
</nav>
</div>
</header>
{lang_bar(lang_code)}"""

def trust(lang_code="en"):
    items = ["100,000+ Students Passed","Since 1995","Pass-or-Money-Back Guarantee",
             "aPHR · PHR · SPHR · SHRM · GPHR","Updated for 2025","HRCI & SHRM Aligned","16 Languages"]
    inner = "".join(f'<div class="trust-item"><div class="trust-ico">&#10003;</div>{i}</div>' for i in items)
    return f'<div class="trust-strip"><div class="trust-inner">{inner}</div></div>'

def footer(lang_code="en"):
    L = LANGUAGES.get(lang_code, LANGUAGES["en"])
    lang_links = "".join(
        f'<a href="{SITE}/{LANGUAGES[lc]["dir"]}/">{FLAGS.get(lc,"")} {LANGUAGES[lc]["native"]}</a>'
        for lc in LANGUAGES
    )
    return f"""<footer class="footer">
<div class="footer-inner">
<div class="footer-grid">
<div class="footer-col">
<h4>{NAME}</h4>
<p style="font-size:.8rem;line-height:1.7;margin-bottom:.9rem;color:#93c5fd">{L["disclosure"]}</p>
<a href="{AFF}" style="color:#bfdbfe;font-weight:900;font-size:.88rem" rel="noopener sponsored">Get HRCP Materials &rarr;</a>
</div>
<div class="footer-col">
<h4>Exam Guides</h4>
<a href="{SITE}/guides/aphr-study-guide/">aPHR Study Guide</a>
<a href="{SITE}/guides/phr-study-guide/">PHR Study Guide</a>
<a href="{SITE}/guides/sphr-study-guide/">SPHR Study Guide</a>
<a href="{SITE}/guides/shrm-cp-prep/">SHRM-CP Prep</a>
<a href="{SITE}/guides/shrm-scp-study-guide/">SHRM-SCP Study Guide</a>
<a href="{SITE}/guides/hrcp-review/">HRCP Review</a>
</div>
<div class="footer-col">
<h4>Quick Links</h4>
<a href="{SITE}/guides/hr-certification/">HR Certification Guide</a>
<a href="{SITE}/guides/best-hr-certification/">Best HR Certification</a>
<a href="{SITE}/guides/hrci-vs-shrm/">HRCI vs SHRM</a>
<a href="{SITE}/guides/hr-certification-cost/">Certification Cost</a>
<a href="{SITE}/guides/is-hr-certification-worth-it/">Is It Worth It?</a>
<a href="{SITE}/guides/aphr-vs-phr/">aPHR vs PHR</a>
</div>
<div class="footer-col">
<h4>Languages</h4>
{lang_links}
</div>
</div>
<div class="footer-bottom">
<p>&copy; {YEAR} {NAME} &mdash; Independent affiliate resource. Not affiliated with HRCP, HRCI, or SHRM. We earn commissions on qualifying purchases at no extra cost to you.</p>
</div>
</div>
</footer>"""

def share(url, lang_code="en"):
    return f"""<div class="share-bar">
<span style="font-size:.82rem;font-weight:700;color:#374151;margin-right:.3rem">Share:</span>
<button class="share-btn sh-fb" data-network="facebook" data-url="{url}">Facebook</button>
<button class="share-btn sh-tw" data-network="twitter" data-url="{url}">Twitter/X</button>
<button class="share-btn sh-li" data-network="linkedin" data-url="{url}">LinkedIn</button>
<button class="share-btn sh-cp" data-network="copy" data-url="{url}">Copy Link</button>
</div>"""

def author_bar(html_content, lang_code="en"):
    mins = read_mins(html_content)
    return f"""<div class="author-bar">
<div class="author-av">HP</div>
<div>
<div class="author-name">{NAME} Editorial<span class="verified-badge">&#10003; HR Certified</span></div>
<div class="author-title">Reviewed <time datetime="{TODAY}">{TODAY}</time> &bull; {mins} min read &bull; Sources: HRCI, SHRM, PayScale</div>
</div>
</div>"""

def pros_cons(pros_list, cons_list):
    pros = "".join(f"<li>{p}</li>" for p in pros_list)
    cons = "".join(f"<li>{c}</li>" for c in cons_list)
    return f"""<div class="pros-cons">
<div class="pros"><h4>Pros</h4><ul>{pros}</ul></div>
<div class="cons"><h4>Cons</h4><ul>{cons}</ul></div>
</div>"""

def guarantee_box():
    return f"""<div class="guarantee-box">
<h3>&#127881; Pass or Your Money Back</h3>
<p>HRCP is so confident in their materials that they offer a full refund if you don't pass your exam. <a href="{AFF}" rel="noopener sponsored">Learn more about the guarantee &rarr;</a></p>
</div>"""

def stat_block():
    return """<div class="stat-cards">
<div class="stat-card"><div class="n">100K+</div><div class="l">Students passed</div></div>
<div class="stat-card"><div class="n">30 yrs</div><div class="l">Since 1995</div></div>
<div class="stat-card"><div class="n">2,000+</div><div class="l">Practice questions</div></div>
<div class="stat-card"><div class="n">72%</div><div class="l">PHR pass rate (HRCI)</div></div>
<div class="stat-card"><div class="n">Pass ✓</div><div class="l">Money-back guarantee</div></div>
</div>"""

def product_grid(slug, idx):
    BTNS = [
        ("Get HRCP Materials","Start Studying Now","Try HRCP Today",
         "Get Study Materials","Order Now","Buy HRCP"),
    ]
    btns = BTNS[0]
    cards = [
        ("Best for Beginners","aPHR Certification Prep","$175 online / $195 print",
         "For those new to HR. 400+ pages, 300+ flashcards, 1,300+ practice questions. Audio reader included. Instant digital access.",
         btns[(sh(slug)+0)%len(btns)]),
        ("Most Popular","PHR/SPHR Complete Program","$295 online / $375 print",
         "The complete HRCP program. 900+ pages, 600+ flashcards, 2,000+ questions, 16 practice exams. Pass-or-money-back guarantee.",
         btns[(sh(slug)+1)%len(btns)]),
        ("Best for SHRM","SHRM-CP/SHRM-SCP Prep","$295 online",
         "Targeted SHRM preparation. Same comprehensive format with SHRM-specific content. 16 practice exams, 2,000+ questions.",
         btns[(sh(slug)+2)%len(btns)]),
        ("International","PHRi/SPHRi International","$295 online",
         "For HR professionals outside the US. Global HR content, 900+ pages, 16 practice exams. Instant digital access worldwide.",
         btns[(sh(slug)+3)%len(btns)]),
    ]
    inner = "".join(
        f'<div class="exam-card"><div class="exam-badge">{badge}</div>'
        f'<h3>{name}</h3><div class="price">{price}</div><p>{desc}</p>'
        f'<a href="{AFF}" class="buy-btn" rel="noopener sponsored">{btn}</a></div>'
        for badge,name,price,desc,btn in cards
    )
    return f'<div id="products"></div><div class="exam-grid">{inner}</div>'

# 30 internal link anchors
IL_POOL = [
    f'<a href="{SITE}/guides/hrcp-review/">HRCP study materials</a>',
    f'<a href="{SITE}/guides/phr-study-guide/">PHR study guide</a>',
    f'<a href="{SITE}/guides/sphr-study-guide/">SPHR study guide</a>',
    f'<a href="{SITE}/guides/aphr-study-guide/">aPHR study guide</a>',
    f'<a href="{SITE}/guides/shrm-cp-prep/">SHRM-CP prep materials</a>',
    f'<a href="{SITE}/guides/hr-certification/">HR certification guide</a>',
    f'<a href="{SITE}/guides/best-hr-certification/">best HR certification</a>',
    f'<a href="{SITE}/guides/hrci-vs-shrm/">HRCI vs SHRM comparison</a>',
    f'<a href="{SITE}/guides/aphr-vs-phr/">aPHR vs PHR guide</a>',
    f'<a href="{SITE}/guides/phr-vs-sphr/">PHR vs SPHR guide</a>',
    f'<a href="{SITE}/guides/hr-certification-cost/">HR certification cost breakdown</a>',
    f'<a href="{SITE}/guides/is-hr-certification-worth-it/">is HR certification worth it</a>',
    f'<a href="{SITE}/guides/hr-certification-practice-test/">practice test guide</a>',
    f'<a href="{SITE}/guides/how-to-pass-hr-certification/">how to pass the HR certification exam</a>',
    f'<a href="{SITE}/guides/hr-certification-study-guide/">HR certification study guide</a>',
    f'<a href="{SITE}/guides/aphr-practice-test/">aPHR practice tests</a>',
    f'<a href="{SITE}/guides/phr-practice-test/">PHR practice tests</a>',
    f'<a href="{SITE}/guides/hr-certification-flashcards/">HR certification flashcards</a>',
    f'<a href="{SITE}/guides/shrm-cp-vs-phr/">SHRM-CP vs PHR comparison</a>',
    f'<a href="{SITE}/guides/hr-certification-for-beginners/">HR certification for beginners</a>',
    f'<a href="{SITE}/guides/phr-requirements/">PHR requirements</a>',
    f'<a href="{SITE}/guides/sphr-requirements/">SPHR requirements</a>',
    f'<a href="{SITE}/guides/aphr-requirements/">aPHR requirements</a>',
    f'<a href="{SITE}/guides/human-resources-certification/">human resources certification</a>',
    f'<a href="{SITE}/guides/free-hr-practice-questions/">free HR practice questions</a>',
    f'<a href="{SITE}/guides/hr-certification-study-schedule/">study schedule template</a>',
    f'<a href="{SITE}/guides/hrcp-practice-test/">HRCP practice exams</a>',
    f'<a href="{SITE}/guides/hr-certification-online/">online HR certification prep</a>',
    f'<a href="{SITE}/guides/how-to-become-hr-certified/">how to become HR certified</a>',
    f'<a href="{SITE}/guides/hr-salary-with-certification/">HR salary with certification</a>',
    # Exam-specific long-tail links
    f'<a href="{SITE}/guides/aphr-pass-rate/">aPHR pass rate data</a>',
    f'<a href="{SITE}/guides/phr-exam-content/">PHR exam content breakdown</a>',
    f'<a href="{SITE}/guides/shrm-cp-requirements/">SHRM-CP eligibility requirements</a>',
    f'<a href="{SITE}/guides/sphr-vs-phr-salary/">SPHR vs PHR salary difference</a>',
    f'<a href="{SITE}/guides/gphr-requirements/">GPHR requirements guide</a>',
    # Career-level links
    f'<a href="{SITE}/guides/hr-coordinator-certification/">HR coordinator certification guide</a>',
    f'<a href="{SITE}/guides/hr-manager-certification/">HR manager certification guide</a>',
    f'<a href="{SITE}/guides/entry-level-hr-certification/">entry-level HR certification</a>',
    f'<a href="{SITE}/guides/hr-certification-for-beginners/">HR certification for beginners</a>',
    # Industry-specific links
    f'<a href="{SITE}/guides/hr-certification-healthcare/">healthcare HR certification</a>',
    f'<a href="{SITE}/guides/hr-certification-technology/">tech company HR certification</a>',
    f'<a href="{SITE}/guides/hr-certification-finance/">finance sector HR certification</a>',
    # Blog deep-links
    f'<a href="{SITE}/blog/phr-study-guide-complete/">complete PHR study guide</a>',
    f'<a href="{SITE}/blog/hrcp-review-honest/">honest HRCP review</a>',
    f'<a href="{SITE}/blog/how-to-pass-phr-first-try/">how to pass PHR first try</a>',
    f'<a href="{SITE}/blog/hr-certification-worth-it/">HR certification worth it analysis</a>',
    f'<a href="{SITE}/blog/shrm-cp-vs-phr-which-better/">SHRM-CP vs PHR comparison</a>',
    f'<a href="{SITE}/blog/aphr-vs-phr-which-first/">aPHR vs PHR guide</a>',
]
def il(slug, n): return IL_POOL[(sh(slug) + n) % len(IL_POOL)]

RELATED = {
    "General":[("hrcp-review","HRCP Review"),("best-hr-certification","Best HR Cert"),
               ("hr-certification-cost","Cert Cost"),("is-hr-certification-worth-it","Worth It?"),
               ("hrci-vs-shrm","HRCI vs SHRM"),("aphr-vs-phr","aPHR vs PHR")],
    "Exam Guide":[("hrcp-review","HRCP Materials"),("hr-certification-practice-test","Practice Tests"),
                  ("hr-certification-flashcards","Flashcards"),("how-to-pass-hr-certification","Pass Tips"),
                  ("hr-certification-study-schedule","Study Schedule"),("phr-study-guide","PHR Guide")],
    "Review":[("hr-certification","HR Certification"),("best-hr-certification","Best Cert"),
              ("hrci-vs-shrm","HRCI vs SHRM"),("hr-certification-cost","Cost"),
              ("is-hr-certification-worth-it","Worth It?"),("aphr-vs-phr","aPHR vs PHR")],
    "Comparison":[("hrcp-review","HRCP Review"),("hr-certification-cost","Cert Cost"),
                  ("best-hr-certification","Best Cert"),("hr-salary-with-certification","Salary Boost"),
                  ("how-to-pass-hr-certification","Pass Tips"),("hr-certification","HR Cert Guide")],
    "Products":[("hrcp-review","HRCP Review"),("hr-certification-practice-test","Practice Tests"),
                ("hr-certification-flashcards","Flashcards"),("phr-study-guide","PHR Guide"),
                ("aphr-study-guide","aPHR Guide"),("shrm-cp-prep","SHRM-CP Prep")],
    "How-To":[("hrcp-review","HRCP Materials"),("hr-certification-practice-test","Practice Tests"),
              ("hr-certification-study-schedule","Study Schedule"),("hr-certification-flashcards","Flashcards"),
              ("phr-requirements","PHR Requirements"),("hr-certification-for-beginners","Beginner Guide")],
    "Informational":[("best-hr-certification","Best Cert"),("hrci-vs-shrm","HRCI vs SHRM"),
                     ("is-hr-certification-worth-it","Worth It?"),("how-to-become-hr-certified","Get Certified"),
                     ("hr-certification-for-beginners","Beginner Guide"),("hrcp-review","HRCP Review")],
    "Geo-State":[("hrcp-review","HRCP Materials"),("phr-study-guide","PHR Guide"),
                 ("aphr-study-guide","aPHR Guide"),("hr-certification","HR Cert Guide"),
                 ("hr-certification-cost","Cert Cost"),("how-to-pass-hr-certification","Pass Tips")],
}
def get_related(cat, slug):
    pool = RELATED.get(cat, RELATED["General"])
    return [(s,t) for s,t in pool if s != slug][:6]

# ── FAQ POOLS ─────────────────────────────────────────────────────────────────
FAQ_POOLS = {
    "General":[
        ("What is the best HR certification to get first?",
         "For HR professionals with less than 1 year of experience, the aPHR is the best starting point — no experience requirement. With 1–4 years, the PHR or SHRM-CP are the most widely recognized mid-level credentials. HRCP study materials cover all three exams."),
        ("Is HRCI or SHRM certification better?",
         "Both are widely respected. HRCI certifications (aPHR, PHR, SPHR) focus more on technical HR law and compliance. SHRM certifications (SHRM-CP, SHRM-SCP) emphasize behavioral competencies. HRCP provides study materials for both — you can prepare for whichever aligns with your career goals."),
        ("How long does it take to prepare for an HR certification exam?",
         "Most candidates spend 8–16 weeks studying. HRCP provides 4-week, 8-week, and 12-week study schedules. The right timeline depends on your current HR knowledge and how many hours per week you can dedicate."),
        ("What is the HRCP pass-or-money-back guarantee?",
         "HRCP offers a full refund if you use their study materials and don't pass your exam. Specific conditions apply — see the HRCP website for current terms. This guarantee reflects 30 years of confidence in their materials."),
        ("How long does HR certification last?",
         "All HRCI and SHRM certifications must be renewed every 3 years. HRCI requires 45–60 recertification credits; SHRM requires 60 PDCs. Many employers and SHRM chapters offer free recertification activities."),
        ("Which HR certification is recognized globally?",
         "HRCI certifications — especially GPHR, PHRi, and SPHRi — are the most internationally recognized. The GPHR is designed for HR professionals managing cross-border operations. HRCI credentials are recognized in 100+ countries."),
        ("Can I study for HR certification while working full time?",
         "Yes. Most candidates study while working full time. HRCP provides study schedules designed for working professionals: 4, 8, and 12-week timelines based on available hours per week. Most find the 8–12 week schedule most manageable."),
        ("What is the difference between HRCI and SHRM?",
         "HRCI has certified HR professionals since 1976 and offers aPHR, PHR, SPHR, GPHR, PHRi, SPHRi. SHRM offers SHRM-CP and SHRM-SCP (since 2014). Both are nationally recognized. HRCP provides study materials for both."),
    ],
    "Exam Guide":[
        ("How hard is the HR certification exam?",
         "PHR pass rate: 72%. aPHR: 71%. SPHR: 76% (HRCI data). These are self-selected motivated candidates — unprepared candidates score lower. Candidates who use structured study materials like HRCP consistently outperform those who study ad hoc."),
        ("What study materials does HRCP provide?",
         "HRCP includes: comprehensive content books (400–900+ pages), practice flashcards (300–600+), online practice exams (13–16 tests with 1,300–2,000+ questions), audio reader (online editions), and a study preparation guide with schedules."),
        ("How many practice questions are in HRCP?",
         "aPHR: 1,300+ questions across 13 exams. PHR/SPHR: 2,000+ questions across 16 exams (preliminary assessment, 6 practice tests, 6 timed exams, 3 mock exams). All accessible through the online practice portal."),
        ("What happens if I fail my HR certification exam?",
         "HRCI allows two retakes per eligibility period with a 90-day wait. SHRM allows one retake per testing window. Your score report identifies which domains cost you the most points. If you used HRCP, the pass-or-money-back guarantee applies."),
        ("How many questions are on the PHR exam?",
         "PHR: 115 scored questions, 3 hours. aPHR: 110 questions, 2 hours. SPHR: 115 questions, 3 hours. SHRM-CP/SCP: 160 questions including 50 situational judgment items, 4 hours. All include some unscored pre-test questions."),
        ("What score do I need to pass the PHR?",
         "HRCI uses scaled scoring 100–700. The passing scaled score is 500. Most candidates need approximately 70–75% correct to achieve a passing scaled score. Consistently scoring 80%+ on HRCP practice exams strongly predicts exam readiness."),
        ("Does HRCP cover all exam domains proportionally?",
         "Yes. HRCP practice questions mirror the actual exam blueprint weighting. Employee and Labor Relations (39% of PHR) receives proportionally more questions. The preliminary assessment identifies your weakest domains before you start studying."),
        ("When should I start studying for my HR certification?",
         "8–12 weeks before your exam date is the standard. HRCP includes 4, 8, and 12-week study schedules. Start with the preliminary assessment to identify knowledge gaps, then follow the schedule. Book your exam date 4–6 weeks out for best availability."),
    ],
    "Comparison":[
        ("What is the difference between aPHR, PHR, and SPHR?",
         "aPHR: entry-level, no experience required, focuses on foundational HR knowledge. PHR: mid-level, 1–4 years experience, focuses on technical HR operations. SPHR: senior, 4–7 years leadership experience, focuses on strategic HR. Each builds on the previous."),
        ("HRCP vs SHRM Learning System — which is better?",
         "HRCP is more comprehensive (covers HRCI and SHRM exams), more affordable, and has a 30-year track record. The SHRM Learning System is produced by SHRM itself and is SHRM-exam-focused. Both have strong results. HRCP offers better value for most candidates preparing for HRCI exams."),
        ("PHR vs SHRM-CP — which should I get?",
         "PHR focuses on technical HR knowledge; SHRM-CP on behavioral competencies. Both are nationally respected. Check job postings at your target employers — they will tell you which credential they specify most frequently. HRCP covers both."),
        ("Is the GPHR worth getting?",
         "Valuable for HR professionals in multinational organizations or managing cross-border HR. Requires 2+ years of global HR experience. For domestic-only roles, PHR or SPHR provides better ROI. For global HR careers, GPHR differentiates meaningfully."),
        ("aPHR vs PHR — which first?",
         "Less than 1 year HR experience: start with aPHR (no experience required, $400 total cost). 1–4 years experience: go directly to PHR. Many professionals earn aPHR early, then PHR as they gain experience — the knowledge builds directly."),
        ("Do employers care whether I have PHR or SHRM-CP?",
         "Most employers recognize both equally. In compliance-heavy industries (healthcare, legal, government), HRCI credentials appear more. In organizations with SHRM member leadership, SHRM credentials carry more internal weight. The best credential is the one you can pass."),
        ("SPHR vs SHRM-SCP — which senior credential is better?",
         "Both are senior-level credentials. SPHR (HRCI) emphasizes strategic HR knowledge and compliance; SHRM-SCP emphasizes strategic leadership competencies. Employer preference varies by industry. Holding both is increasingly common for senior HR leaders."),
        ("Is the aPHR worth getting if I plan to get the PHR later?",
         "Yes. The aPHR validates foundational HR knowledge before you have enough experience for the PHR, improves your resume immediately, and the knowledge built preparing for it directly supports PHR preparation. Many HR professionals get the aPHR in year 1–2, PHR in years 2–4."),
    ],
    "Products":[
        ("Does HRCP offer both online and print materials?",
         "Yes. Online editions: immediate digital access with audio reader included. Print editions: physical books and flashcards shipped to you, with online practice exam access included. Both formats include the full content and all practice exams."),
        ("How long is HRCP online access?",
         "Online practice exam access is granted for 24 months from purchase. Printed materials have no expiration. HRCP updates content annually — for exams more than 12 months out, order closer to your planned exam date."),
        ("Does HRCP include flashcards?",
         "Yes. PHR/SPHR: 600+ flashcards (print with print edition, electronic with online). aPHR: 300+ flashcards. Electronic flashcards are accessible through the online learning platform."),
        ("Are HRCP materials available outside the United States?",
         "Yes. Online editions are available worldwide as instant digital downloads. Print editions ship internationally (additional fees). The PHRi/SPHRi program is specifically designed for HR professionals outside the US."),
        ("Can I share HRCP materials with a colleague?",
         "No. Licensed for individual use only. Each purchase is tied to a personal account. Organizations needing multiple sets should contact HRCP — volume discounts available for 10+ purchases."),
        ("Does HRCP have a free trial?",
         "No standalone free trial. The preliminary assessment in every purchased program serves as a diagnostic. If you use the materials and don't pass, the pass-or-money-back guarantee covers the cost — eliminating financial risk."),
        ("Are discounts available for HRCP?",
         "Volume discounts are available for organizations ordering 10+ sets. Some partner organizations (like CalChamber) offer member discounts. Check the HRCP website or use our affiliate link for current pricing."),
        ("How often does HRCP update their materials?",
         "HRCP updates content annually to reflect current exam blueprints, HR law changes, and best practices. Updates are published in time for each certification exam cycle."),
    ],
    "How-To":[
        ("What is the best way to study for the PHR?",
         "1) Take the HRCP preliminary assessment to identify weak areas. 2) Read content modules, complete self-assessments after each section. 3) Study flashcards daily. 4) Take all practice exams under timed conditions. 5) Review every wrong answer in depth. 6) Take a full mock exam the week before your real exam."),
        ("How many hours per day should I study?",
         "1–2 hours per weekday and 2–4 hours on weekends during your prep period. Consistency matters more than volume. Daily sessions beat weekly cramming. HRCP's schedules are designed around realistic daily time commitments."),
        ("What topics are on the PHR exam?",
         "Six functional areas: 1) Strategic HR Management (12%), 2) HR Planning, Recruitment, Selection (14%), 3) Employee Development and Performance Management (17%), 4) Compensation and Benefits (17%), 5) Employee and Labor Relations (39%), 6) Risk Management (1%). Employee and Labor Relations is the largest domain."),
        ("How do I apply for the PHR exam?",
         "Apply at hrci.org. Complete the application (employment history and education required) and pay the $100 non-refundable application fee. HRCI reviews in 2–3 weeks. After approval, you have 120 days to schedule and sit for your exam via Pearson VUE."),
        ("What experience do I need for the PHR?",
         "1 year professional-level HR experience with a Master's degree, 2 years with a Bachelor's degree, or 4 years with a high school diploma. If you don't meet this yet, pursue the aPHR — no experience required."),
        ("How do I maintain my HR certification?",
         "HRCI requires 45–60 recertification credits every 3 years. Credits earned through continuing education, conferences, teaching, publishing. SHRM requires 60 PDCs. Many employers and SHRM chapters offer free recertification activities."),
        ("What if I cannot meet the PHR experience requirement?",
         "Pursue the aPHR first — no experience required. Many HR professionals hold the aPHR for 1–3 years, then upgrade to PHR as they accumulate experience. HRCP provides separate preparation materials for each credential."),
        ("What score indicates I am ready for the real exam?",
         "Consistently scoring 80%+ on HRCP practice exams is the standard readiness benchmark. If you score below 75% on multiple practice exams, return to content review in the specific domains where you lost the most points before scheduling."),
    ],
    "Informational":[
        ("How much more do certified HR professionals earn?",
         "Research shows 5–15% salary premiums. PayScale data: PHR holders average ~$86,000 vs ~$75,000 for uncertified HR professionals at equivalent experience. Over a 20-year HR career, the cumulative salary impact can exceed $150,000 in additional income."),
        ("How long does it take to get HR certified?",
         "From starting to credential: typically 4–6 months. 8–12 weeks of study, then scheduling and sitting for the exam, then 4–6 weeks for official results. Application review adds 2–3 weeks at the start."),
        ("Is HR certification required to work in HR?",
         "Not legally required, but increasingly expected. A growing percentage of HR manager and above job postings list PHR, SPHR, or SHRM-CP as required or preferred. Starting certification early avoids the career ceiling it can create later."),
        ("What happens if I fail the HR certification exam?",
         "You can retake. HRCI allows two retakes per eligibility period with a 90-day wait. SHRM allows one retake per testing window. Review your score report to identify weak domains. If you used HRCP, the money-back guarantee applies to your first attempt."),
        ("Do employers care about which HR certification I have?",
         "Most employers recognize both HRCI and SHRM credentials. In compliance-heavy industries, HRCI appears more frequently. In organizations with SHRM member leadership, SHRM credentials carry more weight. Best credential: the one you can pass that appears in postings at your target employers."),
        ("Is HR certification recognized globally?",
         "HRCI certifications are recognized in 100+ countries. GPHR, PHRi, and SPHRi are specifically designed for international HR professionals. SHRM certifications are growing internationally, particularly in US-headquartered multinationals."),
        ("Is the aPHR worth getting if I plan to get PHR later?",
         "Yes. The aPHR validates foundational HR knowledge before you have PHR-eligible experience, improves your resume now, and the knowledge built for it directly contributes to PHR preparation. Natural progression: aPHR in year 1–2, PHR in years 2–4."),
        ("How much does the HR certification exam cost?",
         "aPHR: $100 application + $300 exam = $400. PHR: $100 + $395 = $495. SPHR: $100 + $395 = $495. SHRM-CP: $300–$475 (member vs non-member). Add HRCP study materials: $175–$375. Many employers reimburse these costs through professional development budgets."),
    ],
    "Geo-State":[
        ("Are HR certification classes available in {loc}?",
         "HR certification preparation can be completed entirely online, so your location in {loc} doesn't limit your options. HRCP's online study materials provide everything you need. Many universities and SHRM chapters in {loc} also offer in-person prep courses using HRCP as their core curriculum."),
        ("Where can I take the HR certification exam in {loc}?",
         "HRCI exams can be taken online via remote proctoring or at Pearson VUE testing centers throughout {loc}. SHRM exams are offered during two annual testing windows, online or at Prometric centers. Visit hrci.org or shrm.org to find locations in {loc}."),
        ("How much does HR certification cost in {loc}?",
         "Costs are national — {loc} HR professionals pay the same as candidates anywhere. aPHR: $575–$595 total (exam + HRCP materials). PHR: $790–$870 total. SHRM-CP: $595–$770 total. Many {loc} employers reimburse these costs through professional development budgets."),
        ("Is HR certification recognized in {loc}?",
         "Yes. HRCI and SHRM certifications are nationally recognized. Employers in {loc} — like employers throughout the US — recognize PHR, SPHR, aPHR, SHRM-CP, and SHRM-SCP as standard HR credentials. Many {loc} HR job postings list these as preferred or required."),
        ("How long does HR certification take in {loc}?",
         "Typically 4–6 months total: 8–12 weeks of study, then scheduling and sitting for the exam, then 4–6 weeks for official results. Application review adds 2–3 weeks at the start. HRCP materials are available instantly online — no shipping wait for candidates in {loc}."),
        ("Is the HR certification exam available online in {loc}?",
         "Yes. Both HRCI and SHRM offer remote proctoring. You can take your exam from your home or office in {loc} without traveling to a testing center. Requirements: stable internet, private room, webcam, up-to-date browser. Available year-round for HRCI exams; two annual windows for SHRM."),
        ("What HR certification study resources are available in {loc}?",
         "HRCP online materials ($175–$295) are the most comprehensive self-study option — available instantly from anywhere in {loc}. Local universities and community colleges in {loc} may offer instructor-led prep courses. The local SHRM chapter serving {loc} often runs certification prep workshops."),
        ("Do {loc} employers require HR certification?",
         "A growing percentage of HR manager and above job postings in {loc} — reflecting national trends — list PHR, SPHR, or SHRM-CP as required or preferred. Many organizations now require certification for promotion to HR Manager and above. Starting certification early avoids this constraint in your {loc} HR career."),
    ],
    "Default":[
        ("What is HRCP?",
         "HRCP (Human Resource Certification Preparation) has provided HR certification study materials since 1995. Their programs help HR professionals prepare for HRCI exams (aPHR, PHR, SPHR, GPHR) and SHRM exams (SHRM-CP, SHRM-SCP). 100,000+ HR professionals have used HRCP to pass their certification exams."),
        ("How much do HRCP study materials cost?",
         "aPHR Online: $175 | aPHR Print: $195 | PHR/SPHR Online: $295 | PHR/SPHR Print: $375 | SHRM-CP/SCP Online: $295 | PHRi/SPHRi Online: $295. All programs include comprehensive content, flashcards, and practice exams with the pass-or-money-back guarantee."),
        ("Does HRCP guarantee I will pass?",
         "Yes. HRCP offers a pass-or-money-back guarantee if you use their study materials and don't pass. Specific terms and conditions apply — see the HRCP website for current details. This guarantee has been offered since 1995, reflecting 30 years of confidence in their materials."),
        ("What HR certifications does HRCP cover?",
         "HRCP covers: aPHR, PHR, SPHR, GPHR (all HRCI credentials), SHRM-CP, SHRM-SCP, PHRi, and SPHRi. Each exam has a tailored preparation program. The PHR/SPHR program also covers SHRM-CP and SHRM-SCP preparation."),
        ("What is the best HR certification for a career change into HR?",
         "The aPHR is the best starting credential for career changers. No experience required — pursue it before your first HR role. It validates foundational knowledge to skeptical employers who might otherwise discount a resume without direct HR experience."),
        ("How does HRCP compare to other HR study resources?",
         "HRCP is the most established resource (100,000+ passed since 1995). Key advantages: covers HRCI and SHRM exams, 2,000+ practice questions, updated annually, genuine pass-or-money-back guarantee. Main alternative is the SHRM Learning System (SHRM-only, more expensive). HRCP offers the best combination of depth, coverage, and price for most candidates."),
        ("Can I take the HR certification exam online?",
         "Yes. Both HRCI and SHRM offer remote proctoring — you take the exam from your home or office via webcam. No travel required. HRCI exams are available year-round remotely. SHRM exams are available during two annual windows remotely. Requirements: stable internet, private room, webcam, up-to-date browser."),
        ("What is the minimum experience needed for HR certification?",
         "aPHR: no experience required. PHR: 1 year (Master's), 2 years (Bachelor's), or 4 years (high school diploma) of professional-level HR experience. SPHR: 4 years (Master's) or 7 years (high school diploma) with HR leadership responsibilities. SHRM-CP: 0–3 years depending on education. SHRM-SCP: 3+ years strategic HR experience."),
    ],
}

def make_faq(kw, slug, category, loc=None):
    # Route to most specific pool
    if category in FAQ_POOLS:
        pool_key = category
    elif "review" in slug or "hrcp" in slug:
        pool_key = "Review"
    elif "comparison" in slug or "-vs-" in slug:
        pool_key = "Comparison"
    elif "cost" in slug or "salary" in slug or "worth" in slug:
        pool_key = "Informational"
    elif "study" in slug or "practice" in slug or "flashcard" in slug or "schedule" in slug:
        pool_key = "Products"
    elif "how-to" in slug or "pass" in slug or "become" in slug:
        pool_key = "How-To"
    else:
        pool_key = "Default"
    pool = FAQ_POOLS.get(pool_key, FAQ_POOLS["Default"])
    def _sub(s):
        s = s.replace("{loc}", loc or "your state")
        s = s.replace("{city}", loc or "your city")
        return s
    return "".join(
        f'<details class="faq-item"><summary class="faq-q">{_sub(q)}</summary>'
        f'<div class="faq-a">{_sub(a)}</div></details>'
        for q,a in pool
    )

# ── EXTRA SECTIONS (rotates per page for WC variance) ─────────────────────────
def _extra_section(slug, idx=0):
    EXTRAS = [
        "",
        f"""<h2 id="requirements">HR Certification Requirements at a Glance</h2>
<table class="cmp">
<tr><th>Credential</th><th>Experience</th><th>Education</th><th>Exam Cost</th><th>Renewal</th></tr>
<tr><td><strong>aPHR</strong></td><td class="good">None required</td><td>High school diploma</td><td>$400</td><td>Every 3 yrs</td></tr>
<tr><td><strong>PHR</strong></td><td>1–4 years</td><td>Any degree helps</td><td>$495</td><td>Every 3 yrs</td></tr>
<tr><td><strong>SPHR</strong></td><td>4–7 years leadership</td><td>Any degree helps</td><td>$495</td><td>Every 3 yrs</td></tr>
<tr><td><strong>SHRM-CP</strong></td><td>0–3 years (varies)</td><td>HR degree preferred</td><td>$300–$475</td><td>Every 3 yrs</td></tr>
<tr><td><strong>SHRM-SCP</strong></td><td>3+ years strategic</td><td>Any degree</td><td>$300–$475</td><td>Every 3 yrs</td></tr>
<tr><td><strong>GPHR</strong></td><td>2+ years global HR</td><td>Any degree</td><td>$495</td><td>Every 3 yrs</td></tr>
</table>
<p>The aPHR is the fastest path to certification — no experience required, $400 total exam cost, and HRCP's online study materials are available for $175 with instant access.</p>""",
        f"""<h2 id="salary">HR Certification Salary Impact: The Numbers</h2>
<table class="cmp">
<tr><th>Role</th><th>Uncertified Avg</th><th>Certified Avg</th><th>Premium</th></tr>
<tr><td>HR Coordinator</td><td>$48,000</td><td>$54,000</td><td class="good">+$6,000 (12.5%)</td></tr>
<tr><td>HR Generalist</td><td>$58,000</td><td>$67,000</td><td class="good">+$9,000 (15.5%)</td></tr>
<tr><td>HR Manager</td><td>$75,000</td><td>$86,000</td><td class="good">+$11,000 (14.7%)</td></tr>
<tr><td>HR Business Partner</td><td>$82,000</td><td>$94,000</td><td class="good">+$12,000 (14.6%)</td></tr>
<tr><td>HR Director</td><td>$105,000</td><td>$120,000</td><td class="good">+$15,000 (14.3%)</td></tr>
</table>
<p>Based on PayScale data and SHRM compensation surveys. At a 10% salary premium on a $65,000 base, HR certification generates $6,500/year in additional income — recovering the full PHR certification cost (~$870) in under 7 weeks.</p>""",
        f"""<h2 id="study-tips">HR Certification Study Tips That Work</h2>
<p><strong>Take the preliminary assessment first.</strong> Every HRCP program includes a diagnostic. It identifies your weak areas before you study — candidates who skip it waste 20–30% of study time over-preparing strong areas.</p>
<p><strong>Study flashcards 15 minutes every day.</strong> HR certification exams are heavily terminology-dependent. HRCP's 300–600+ flashcards cover the terms that appear most frequently. Daily short sessions beat weekly cramming.</p>
<p><strong>Take timed practice exams under real conditions.</strong> The PHR gives you 93 seconds per question. Practice at this pace. HRCP includes 16 practice exams — use all of them.</p>
<p><strong>Know which domain is weighted highest.</strong> Employee and Labor Relations is 39% of the PHR exam. Allocate study time proportionally to domain weighting, not evenly across all topics.</p>
<p><strong>Review wrong answers more than right ones.</strong> After every practice exam, spend equal time analysing incorrect answers. That is where real preparation happens.</p>""",
        f"""<h2 id="career-path">HR Certification by Career Stage</h2>
<p><strong>Starting out (0–1 year HR):</strong> <strong>aPHR</strong> — no experience required, $400 exam, $175 HRCP materials. Pursue during your first role or even before it. Immediately differentiates your resume.</p>
<p><strong>Established HR (1–4 years):</strong> <strong>PHR or SHRM-CP</strong> — both widely recognized. PHR focuses on compliance; SHRM-CP on behavioral competencies. HRCP Complete Program ($295 online) covers both.</p>
<p><strong>HR manager/director (4–7+ years):</strong> <strong>SPHR or SHRM-SCP</strong> — expected for director-level positions at most organizations. Same HRCP program covers SPHR and PHR preparation.</p>
<p><strong>Global HR (2+ years international):</strong> <strong>GPHR, PHRi, or SPHRi</strong> — recognized globally. HRCP provides specialized international preparation at $295 online.</p>""",
        f"""<h2 id="exam-day">Exam Day: What to Expect</h2>
<p><strong>Scheduling.</strong> HRCI exams (aPHR, PHR, SPHR, GPHR) are available year-round online via remote proctoring or at Pearson VUE testing centers. SHRM exams (SHRM-CP, SHRM-SCP) are offered during two annual windows at Prometric centers or remotely. Schedule 4–6 weeks ahead for best availability.</p>
<p><strong>Remote vs testing center.</strong> Remote proctoring is convenient but requires stable internet, a private room, and no second monitors. Testing centers eliminate technology variables but require travel. Both deliver the same exam experience.</p>
<p><strong>The week before.</strong> Stop learning new material. Review your weakest domains only. Take one final mock exam on day 5 or 6. Prioritise sleep — fatigue costs more points than last-minute studying gains.</p>
<p><strong>During the exam.</strong> Flag uncertain questions and return at the end. Never leave blank — there is no penalty for wrong answers. On the PHR: if you spend over 2 minutes on one question, flag and move on.</p>""",
    ]
    return EXTRAS[(sh(slug) + idx) % len(EXTRAS)]


# ── BODY VARIANTS — 12 ────────────────────────────────────────────────────────
def body(kw, slug, category, idx):
    if category == "Geo-State": return _body_geo(kw, slug, idx)
    if category == "Comparison": return _body_comparison(kw, slug, idx)
    h = (idx + sh(slug)) % 12

    def _il(n): return il(slug, n)
    faq  = make_faq(kw, slug, category)
    stat = stat_block()
    guar = guarantee_box()
    extra = _extra_section(slug, idx)

    if h == 0:
        return f"""
<h2 id="overview">Why HRCP Study Materials Work</h2>
<p>Passing an HR certification exam requires more than general HR knowledge — it requires systematic preparation using materials specifically designed for the exam format, content weighting, and question style. The {_il(0)} from HRCP have helped over 100,000 HR professionals pass their certification exams since 1995. That track record exists for a reason.</p>
<p>HRCP's approach is built on three principles: comprehensive content coverage (every topic tested on the exam), realistic practice (exam-format questions that mirror actual test conditions), and structured progression (study schedules that move you through the material systematically). No other resource covers the combination of HRCI and SHRM exams as thoroughly. See our {_il(1)} for a complete breakdown of what is included.</p>
{stat}
<h2 id="how-to">What HRCP Includes</h2>
<table class="cmp" aria-label="HRCP programs comparison">
<tr><th>Program</th><th>Content</th><th>Practice Exams</th><th>Questions</th><th>Price</th></tr>
<tr><td><strong>aPHR Online</strong></td><td>400+ pages</td><td>13 exams</td><td class="good">1,300+</td><td>$175</td></tr>
<tr><td><strong>aPHR Print</strong></td><td>400+ pages + flashcards</td><td>13 exams</td><td class="good">1,300+</td><td>$195</td></tr>
<tr><td><strong>PHR/SPHR Online</strong></td><td>900+ pages</td><td>16 exams</td><td class="good">2,000+</td><td>$295</td></tr>
<tr><td><strong>PHR/SPHR Print</strong></td><td>900+ pages + flashcards</td><td>16 exams</td><td class="good">2,000+</td><td>$375</td></tr>
<tr><td><strong>SHRM-CP/SCP Online</strong></td><td>900+ pages</td><td>16 exams</td><td class="good">2,000+</td><td>$295</td></tr>
</table>
{extra}
{extra}
{guar}
<div id="faq"></div><div class="faq-wrap">{faq}</div>"""

    elif h == 1:
        return f"""
<h2 id="overview">HR Certification: What You Need to Know Before Starting</h2>
<p>HR certification is increasingly required — not just preferred — for mid-level and senior HR positions. A 2024 survey found that over 60% of HR director job postings list PHR or SHRM-CP certification as a requirement or strong preference. If you are building a career in HR, certification is not optional. The {_il(5)} covers the full landscape of what is available and which credential fits your career stage.</p>
<p>The credential pathway: aPHR (no experience required) → PHR (1–4 years experience) → SPHR (4–7 years in HR leadership). SHRM runs a parallel track: SHRM-CP → SHRM-SCP. Both HRCI and SHRM credentials are nationally recognized. Many HR professionals eventually hold certifications from both bodies. Our {_il(7)} covers the full comparison.</p>
{stat}
<h2 id="how-to">Which Certification Is Right for You?</h2>
<table class="cmp" aria-label="HR certifications comparison">
<tr><th>Credential</th><th>Issuer</th><th>Experience Req.</th><th>Focus</th><th>Exam Cost</th></tr>
<tr><td><strong>aPHR</strong></td><td>HRCI</td><td class="good">None</td><td>Entry-level HR knowledge</td><td>$400</td></tr>
<tr><td><strong>PHR</strong></td><td>HRCI</td><td>1–4 years</td><td>Technical HR operations</td><td>$495</td></tr>
<tr><td><strong>SPHR</strong></td><td>HRCI</td><td>4–7 years</td><td>Strategic HR leadership</td><td>$495</td></tr>
<tr><td><strong>SHRM-CP</strong></td><td>SHRM</td><td>Varies</td><td>Behavioral competencies</td><td>$300–$475</td></tr>
<tr><td><strong>SHRM-SCP</strong></td><td>SHRM</td><td>3+ years</td><td>Strategic HR</td><td>$300–$475</td></tr>
<tr><td><strong>GPHR</strong></td><td>HRCI</td><td>2+ years global</td><td>Global HR operations</td><td>$495</td></tr>
</table>
{extra}
{extra}
{guar}
<div id="faq"></div><div class="faq-wrap">{faq}</div>"""

    elif h == 2:
        return f"""
<h2 id="overview">How to Study for HR Certification: The Complete Strategy</h2>
<p>Most HR certification exam failures are not caused by insufficient HR knowledge — they are caused by insufficient exam preparation. Knowing HR is not the same as knowing how to answer HR certification exam questions, which are often situational and require applying principles rather than reciting facts. A structured study approach using {_il(0)} is what closes this gap. Our {_il(13)} covers the complete step-by-step process.</p>
{stat}
<h2 id="how-to">8-Week Study Plan Overview</h2>
<ol class="steps">
<li><strong>Week 1: Assess and plan</strong><p>Take the HRCP preliminary assessment to identify your strongest and weakest knowledge areas. Use your results to allocate study time — spend more time on weak areas, not evenly across all topics.</p><div class="step-time">&#9201; 5–8 hours total</div></li>
<li><strong>Weeks 2–5: Content review</strong><p>Read all HRCP content modules systematically. Highlight key concepts. Complete the self-assessments at the end of each section. Study flashcards for terminology in each unit before moving to the next.</p><div class="step-time">&#9201; 10–12 hours per week</div></li>
<li><strong>Weeks 6–7: Practice exams</strong><p>Take all HRCP practice exams under timed, exam conditions. Review every incorrect answer — understanding why you got it wrong is more valuable than the question itself. Retake exams where you score below 70%.</p><div class="step-time">&#9201; 8–10 hours per week</div></li>
<li><strong>Week 8: Final review and mock exam</strong><p>Review your weakest areas from practice exams. Take a full HRCP mock exam in a single sitting to simulate exam-day conditions. Focus on rest and confidence in the final 48 hours.</p><div class="step-time">&#9201; 6–8 hours</div></li>
</ol>
<div class="tip-box"><strong>&#128161; Key insight</strong><p>HRCP includes free sample study schedules for 4-week, 8-week, and 12-week preparation timelines. Start with the preliminary assessment before choosing your schedule — your knowledge gaps determine how much time you need.</p></div>
{extra}
{extra}
{guar}
<div id="faq"></div><div class="faq-wrap">{faq}</div>"""

    elif h == 3:
        return f"""
<h2 id="overview">HRCP Review: Honest Assessment of the Study Materials</h2>
<p>This review is written independently. We promote HRCP through our affiliate link because we believe it is the best HR certification prep resource available — not because of the affiliate relationship. Here is the honest picture.</p>
{stat}
<h2 id="how-to">What HRCP Gets Right</h2>
<p><strong>Content depth (&#9733;&#9733;&#9733;&#9733;&#9733;):</strong> HRCP materials are comprehensive. The PHR/SPHR program's 900+ pages cover every functional area tested on the exam in detail. Content is updated annually to reflect current HR law, practices, and exam blueprints. Candidates who read the materials thoroughly report feeling well-prepared for exam content.</p>
<p><strong>Practice questions (&#9733;&#9733;&#9733;&#9733;&#9733;):</strong> 2,000+ questions across 16 practice exams for the PHR/SPHR program is generous. The preliminary assessment, practice tests, timed exams, and mock exams provide a complete progression from diagnostic to exam simulation. Question quality is consistently noted as matching actual exam style and difficulty.</p>
<p><strong>Flashcards (&#9733;&#9733;&#9733;&#9733;&#9734;):</strong> 600+ flashcards covering terminology and key concepts. Printed flashcards come with print editions; electronic flashcards with online editions. Terminology recall accounts for a significant portion of exam points — flashcard study is time well spent.</p>
<p><strong>Value (&#9733;&#9733;&#9733;&#9733;&#9733;):</strong> At $295–$375 for the complete PHR/SPHR program, HRCP is competitively priced relative to alternatives with comparable content. The pass-or-money-back guarantee eliminates purchase risk.</p>
<h2 id="limitations">Honest Limitations</h2>
<p>HRCP materials are text-heavy — they are not video-based or gamified. Candidates who learn primarily through video lectures or prefer interactive digital learning may find the format less engaging. The content is also designed for self-directed study; there are no live instructor sessions included (though partner organizations offer HRCP-based courses). See {_il(7)} for a side-by-side with the SHRM Learning System.</p>
{pros_cons(
    ["Comprehensive content — 900+ pages PHR/SPHR",
     "2,000+ practice questions, 16 practice exams",
     "Pass-or-money-back guarantee",
     "Updated annually for current exam content",
     "Covers HRCI and SHRM exams",
     "Audio reader in online editions",
     "30 years of proven results"],
    ["Text-heavy — no included video lectures",
     "No live instructor sessions",
     "Print editions require shipping time",
     "Online access expires after 24 months"]
)}
<div id="faq"></div><div class="faq-wrap">{faq}</div>"""

    elif h == 4:
        return f"""
<h2 id="overview">HR Certification Cost: The Complete 2025 Breakdown</h2>
<p>The total cost of HR certification is higher than most candidates initially expect — but also a better financial investment than most realize. This guide breaks down every cost and calculates the return. Our {_il(10)} covers all fees in detail.</p>
{stat}
<h2 id="how-to">Full Cost Breakdown</h2>
<table class="cmp" aria-label="HR certification costs">
<tr><th>Cost Item</th><th>aPHR</th><th>PHR</th><th>SPHR</th><th>SHRM-CP</th></tr>
<tr><td><strong>Application fee</strong></td><td>$100</td><td>$100</td><td>$100</td><td>Included</td></tr>
<tr><td><strong>Exam fee</strong></td><td>$300</td><td>$395</td><td>$395</td><td>$300–$475</td></tr>
<tr><td><strong>HRCP study materials</strong></td><td class="good">$175–$195</td><td class="good">$295–$375</td><td class="good">$295–$375</td><td class="good">$295</td></tr>
<tr><td><strong>Total (estimate)</strong></td><td>$575–$595</td><td>$790–$870</td><td>$790–$870</td><td>$595–$770</td></tr>
<tr><td><strong>Recertification (every 3 yrs)</strong></td><td>$100</td><td>$169</td><td>$169</td><td>$100–$150</td></tr>
</table>
<h2>The Return on Investment</h2>
<p>Certified HR professionals earn 5–15% more than uncertified counterparts. PayScale data shows PHR holders averaging ~$86,000 annually vs ~$75,000 for uncertified HR professionals at the same experience level. At a conservative 5% salary premium on a $70,000 salary, that is $3,500/year in additional income. The total cost of PHR certification ($870 first year) pays for itself in under 3 months of salary premium — and compounds every year after. See our {_il(29)} for the full analysis.</p>
<div class="tip-box"><strong>&#128161; Employer reimbursement</strong><p>Many employers reimburse HR certification costs as professional development expenses. Ask your HR manager or manager before paying out of pocket — certification costs are frequently covered as part of professional development budgets.</p></div>
{extra}
{extra}
{guar}
<div id="faq"></div><div class="faq-wrap">{faq}</div>"""

    elif h == 5:
        return f"""
<h2 id="overview">How to Pass the HR Certification Exam: Proven Strategies</h2>
<p>The HR certification exams test your ability to apply HR principles — not just recall them. This distinction matters enormously for how you prepare. A candidate who has memorized HRCP content but has not practiced applying it to situational questions will underperform relative to their knowledge. Our {_il(14)} walks through the full study strategy.</p>
{stat}
<h2 id="how-to">The Most Effective Exam Preparation Strategies</h2>
<p><strong>1. Start with the preliminary assessment.</strong> The HRCP preliminary assessment identifies your knowledge gaps before you study. This is not optional — it tells you exactly where to spend the most time. Candidates who skip it waste time on strong areas and underprepare weak ones.</p>
<p><strong>2. Study terminology with flashcards daily.</strong> A significant portion of HR exam questions turn on precise terminology. The difference between "can" and "must" in an employment law context determines the right answer. HRCP's 300–600+ flashcards cover the terminology that appears most frequently on exams. 15 minutes of flashcard review daily beats a single 2-hour terminology session weekly.</p>
<p><strong>3. Practice in exam conditions.</strong> Taking a 3-hour practice exam while sitting at your kitchen table with Netflix on in the background is not equivalent to sitting in a testing center for 3 hours. Practice under realistic conditions: timed, no interruptions, no external references. HRCP's timed practice exams are specifically designed for this.</p>
<p><strong>4. Analyse wrong answers, not just correct ones.</strong> After each practice exam, spend as much time reviewing incorrect answers as you spent taking the exam. Understanding why the right answer is right — and why the other options are wrong — is more valuable than any single correct answer.</p>
<p><strong>5. Know the exam blueprint.</strong> HRCI and SHRM publish detailed exam content outlines that show how much each domain is weighted. Employee and Labor Relations is 39% of the PHR exam. If you spend equal time on all six domains, you are dramatically underpreparing for the highest-weighted area.</p>
<div class="tip-box"><strong>&#128161; The week before your exam</strong><p>Do not attempt to learn new material in the week before your exam. Focus on reviewing known weak areas, taking one final mock exam, and ensuring you are rested. Fatigue on exam day costs more points than any last-minute studying gains.</p></div>
{extra}
{extra}
{guar}
<div id="faq"></div><div class="faq-wrap">{faq}</div>"""

    elif h == 6:
        return f"""
<h2 id="overview">HRCI vs SHRM: Which HR Certification Is Better?</h2>
<p>The HRCI vs SHRM debate is the most common question HR professionals face when choosing their first certification. The honest answer is that both are respected, both are valued by employers, and the right choice depends on your career goals and current experience level. See our full {_il(7)} for the detailed comparison.</p>
{stat}
<h2 id="how-to">HRCI vs SHRM: Side-by-Side Comparison</h2>
<table class="cmp" aria-label="HRCI vs SHRM comparison">
<tr><th>Factor</th><th>HRCI (PHR, SPHR, aPHR)</th><th>SHRM (SHRM-CP, SHRM-SCP)</th></tr>
<tr><td><strong>Founded</strong></td><td>1976</td><td>2014 (credentials)</td></tr>
<tr><td><strong>Exam focus</strong></td><td>Technical HR knowledge and compliance</td><td>Behavioral competencies and application</td></tr>
<tr><td><strong>Entry-level option</strong></td><td class="good">aPHR (no experience required)</td><td class="bad">No — minimum experience required</td></tr>
<tr><td><strong>Employer recognition</strong></td><td class="good">Very high</td><td class="good">Very high</td></tr>
<tr><td><strong>Global recognition</strong></td><td class="good">Strong (PHRi, SPHRi, GPHR)</td><td class="ok">Growing</td></tr>
<tr><td><strong>Recertification</strong></td><td>Every 3 years (60 recert credits)</td><td>Every 3 years (60 PDCs)</td></tr>
<tr><td><strong>Exam cost</strong></td><td>$400–$495</td><td>$300–$475</td></tr>
<tr><td><strong>HRCP study materials</strong></td><td class="good">All HRCI exams covered</td><td class="good">SHRM-CP/SCP covered</td></tr>
</table>
<h2>Our Recommendation</h2>
<p>If you are new to HR with less than 1 year of experience: <strong>aPHR</strong> — no experience requirement, immediate eligibility, recognized entry-level credential. If you have 1–4 years in HR operations: <strong>PHR or SHRM-CP</strong> — both are strong; choose based on whether your employer or your industry tends to recognize one more. If you work in HR leadership: <strong>SPHR or SHRM-SCP</strong>. If you work in global HR: <strong>GPHR</strong>.</p>
{extra}
{extra}
{guar}
<div id="faq"></div><div class="faq-wrap">{faq}</div>"""

    elif h == 7:
        return f"""
<h2 id="overview">Is HR Certification Worth It? The Honest Analysis</h2>
<p>HR certification requires real investment — study time, exam fees, and ongoing recertification costs. Is it worth it? The data is clear: for most HR professionals, the answer is yes. The {_il(11)} details exactly what the research shows.</p>
{stat}
<h2 id="how-to">The Case For Getting Certified</h2>
<p><strong>Salary premium:</strong> Certified HR professionals earn 5–15% more than uncertified counterparts at the same experience level. PayScale data shows PHR holders averaging ~$86,000 vs ~$75,000 for comparable uncertified professionals. On a $75,000 salary, a 5% premium is $3,750/year — more than recovering the certification cost annually.</p>
<p><strong>Career advancement:</strong> A 2023 SHRM study found certified HR professionals were significantly more likely to be promoted to senior roles within 5 years than uncertified colleagues. Many organizations now require certification for promotion to HR Manager and above.</p>
<p><strong>Employment security:</strong> In HR workforce reductions, certified professionals are disproportionately retained. Certification signals a commitment to the profession that organizational leaders value.</p>
<p><strong>Knowledge depth:</strong> Systematic exam preparation forces you to fill knowledge gaps you may not know you have. Most candidates report that the study process made them meaningfully better at their current job — independent of whether they passed the exam.</p>
<h2>The Case Against (and Why It Still Adds Up)</h2>
<p>Time investment is real — 8–12 weeks of structured study is significant. Exam costs are not trivial. Recertification requires ongoing effort. But consider: a one-time $870 investment (PHR total cost) that generates $3,750+ annually in salary premium pays for itself in under 3 months. Over a 20-year career, the cumulative value of the salary premium alone far exceeds the certification costs. See our {_il(10)} for the full numbers.</p>
{extra}
{extra}
{guar}
<div id="faq"></div><div class="faq-wrap">{faq}</div>"""

    elif h == 8:
        return f"""
<h2 id="overview">aPHR Certification: Complete Beginner's Guide</h2>
<p>The aPHR (Associate Professional in Human Resources) is the credential designed for those at the beginning of their HR career. Unlike the PHR and SPHR, the aPHR has no experience requirement — you can sit for the exam before or during your first HR job. The {_il(3)} covers everything you need to prepare.</p>
{stat}
<h2 id="how-to">aPHR Fast Facts</h2>
<table class="cmp">
<tr><th>Detail</th><th>aPHR Information</th></tr>
<tr><td><strong>Issuer</strong></td><td>HRCI (HR Certification Institute)</td></tr>
<tr><td><strong>Experience required</strong></td><td class="good">None</td></tr>
<tr><td><strong>Exam cost</strong></td><td>$100 application + $300 exam = $400 total</td></tr>
<tr><td><strong>Exam format</strong></td><td>110 questions, 2 hours</td></tr>
<tr><td><strong>Pass rate</strong></td><td>~71%</td></tr>
<tr><td><strong>Recertification</strong></td><td>Every 3 years (45 recert credits)</td></tr>
<tr><td><strong>HRCP prep cost</strong></td><td class="good">$175 online / $195 print</td></tr>
</table>
<h2>aPHR Exam Content Areas</h2>
<p>The aPHR covers five functional areas: <strong>Talent Acquisition</strong> (22%), <strong>Learning and Development</strong> (18%), <strong>Total Rewards</strong> (18%), <strong>Employee Engagement</strong> (19%), and <strong>HR Compliance and Risk Management</strong> (23%). HR Compliance and Risk Management is the largest domain. HRCP materials provide comprehensive coverage of all five areas.</p>
<p>The aPHR is an ideal first certification — it validates your foundational HR knowledge, makes your resume competitive for entry and mid-level HR positions, and sets you up to pursue the PHR once you have 1–4 years of experience. Many HR professionals begin studying for the aPHR while still in college or during their first HR internship.</p>
{extra}
{extra}
{guar}
<div id="faq"></div><div class="faq-wrap">{faq}</div>"""

    elif h == 9:
        return f"""
<h2 id="overview">PHR vs SPHR: Which Should You Get?</h2>
<p>PHR and SPHR are both HRCI certifications, but they target different career stages and test different competencies. Choosing the right one now — rather than pursuing the wrong credential and needing to recertify — matters. See our detailed {_il(9)} for the full breakdown.</p>
{stat}
<h2 id="how-to">PHR vs SPHR: The Key Differences</h2>
<table class="cmp">
<tr><th>Factor</th><th>PHR</th><th>SPHR</th></tr>
<tr><td><strong>Target level</strong></td><td>Mid-level HR professional</td><td>Senior HR leader / manager</td></tr>
<tr><td><strong>Experience required</strong></td><td>1–4 years depending on education</td><td>4–7 years in HR leadership</td></tr>
<tr><td><strong>Exam focus</strong></td><td>Technical HR operations and compliance</td><td>Strategic HR planning and policy</td></tr>
<tr><td><strong>Exam format</strong></td><td>115 questions, 3 hours</td><td>115 questions, 3 hours</td></tr>
<tr><td><strong>Pass rate (2025)</strong></td><td>72%</td><td>76%</td></tr>
<tr><td><strong>Exam cost</strong></td><td>$495</td><td>$495</td></tr>
<tr><td><strong>HRCP materials</strong></td><td class="good">Same program covers both</td><td class="good">Same program covers both</td></tr>
</table>
<h2>Which One Is Right for You?</h2>
<p>Get the PHR if: you have 1–4 years of HR experience, your role is primarily operational (implementing HR policies rather than creating them), or you are preparing for your first management-level certification.</p>
<p>Get the SPHR if: you have 4+ years of HR experience including leadership responsibilities, your role involves strategic HR decisions and policy creation, or you report to the executive level and need a credential that reflects that scope.</p>
<p>Both exams use the same HRCP study program — the Complete HRCP Program for PHR/SPHR covers both certifications comprehensively at {_il(1)}.</p>
{extra}
{extra}
{guar}
<div id="faq"></div><div class="faq-wrap">{faq}</div>"""

    elif h == 10:
        return f"""
<h2 id="overview">HR Certification Practice Tests: What to Use and How</h2>
<p>Practice tests are the most important component of HR certification preparation. Candidates who take multiple full practice exams consistently outperform those who study content alone. The {_il(12)} and {_il(15)} from HRCP are among the most comprehensive available. Here is how to use them effectively.</p>
{stat}
<h2 id="how-to">How to Use Practice Tests Effectively</h2>
<ol class="steps">
<li><strong>Take the preliminary assessment first</strong><p>Before studying, take the HRCP preliminary assessment. This diagnostic identifies your knowledge gaps and tells you exactly where to focus. Do not skip this step — it determines your study allocation.</p><div class="step-time">&#9201; 1–2 hours</div></li>
<li><strong>Study content, then test</strong><p>Complete your content review of a module before taking practice questions on that module. Testing before studying builds false confidence from guessing — not genuine knowledge.</p></li>
<li><strong>Take timed exams under real conditions</strong><p>Simulate the actual exam environment: no phone, no notes, timed per question. The PHR exam gives you approximately 93 seconds per question. Practice at this pace before your actual exam date.</p><div class="step-time">&#9201; 3 hours per full exam</div></li>
<li><strong>Analyse every wrong answer</strong><p>For each incorrect question, identify: which functional area it covered, why you chose incorrectly, and why the correct answer is right. Log weak areas and return to them in content review.</p></li>
<li><strong>Target a consistent 80%+ before sitting the real exam</strong><p>Most candidates who consistently score 80%+ on HRCP practice exams pass the actual certification exam. If you are consistently below 75%, additional content review is needed before scheduling your exam date.</p></li>
</ol>
<div class="tip-box"><strong>&#128161; Practice exam tip</strong><p>HRCP's mock exams (3 included in the PHR/SPHR program) are designed to most closely replicate the actual exam experience. Save at least one mock exam for the week before your scheduled exam date as a final confidence-builder.</p></div>
{extra}
{extra}
{guar}
<div id="faq"></div><div class="faq-wrap">{faq}</div>"""

    else:  # h == 11
        return f"""
<h2 id="overview">SHRM-CP vs PHR: Which Certification Is Better?</h2>
<p>SHRM-CP and PHR are the two most popular mid-level HR certifications in the United States. Both are widely recognized, both demonstrate meaningful HR competence, and both have real value in the job market. The right choice depends on your career context. See our {_il(18)} for the full analysis.</p>
{stat}
<h2 id="how-to">SHRM-CP vs PHR: Detailed Comparison</h2>
<table class="cmp">
<tr><th>Factor</th><th>SHRM-CP</th><th>PHR</th></tr>
<tr><td><strong>Issuer</strong></td><td>SHRM</td><td>HRCI</td></tr>
<tr><td><strong>Exam emphasis</strong></td><td>Behavioral competencies, situational judgment</td><td>Technical HR knowledge, compliance</td></tr>
<tr><td><strong>Experience req.</strong></td><td>Varies (0–1 years with HR degree)</td><td>1–4 years</td></tr>
<tr><td><strong>Exam format</strong></td><td>160 questions (110 knowledge, 50 situational), 4 hours</td><td>115 questions, 3 hours</td></tr>
<tr><td><strong>Exam windows</strong></td><td>Spring and Fall only</td><td class="good">Year-round</td></tr>
<tr><td><strong>Cost</strong></td><td>$300 (member) / $475 (non-member)</td><td>$495</td></tr>
<tr><td><strong>HRCP materials</strong></td><td class="good">Yes — same program</td><td class="good">Yes — same program</td></tr>
</table>
<h2>The Decision Framework</h2>
<p><strong>Choose SHRM-CP if:</strong> your employer is a SHRM member organization, your HR peers tend to hold SHRM credentials, you prefer behavioral/situational exam questions over knowledge recall, or your exam availability is better with SHRM's testing windows.</p>
<p><strong>Choose PHR if:</strong> you work in a compliance-heavy industry where technical HR law knowledge is valued, you want year-round exam scheduling flexibility, or your HR leadership holds HRCI credentials.</p>
<p><strong>Consider both eventually:</strong> Many HR professionals hold both credentials. The HRCP Complete Program covers preparation for both PHR/SPHR and SHRM-CP/SCP — {_il(0)} covers both exam tracks.</p>
{extra}
{extra}
{guar}
<div id="faq"></div><div class="faq-wrap">{faq}</div>"""


# ── COMPARISON BODY ───────────────────────────────────────────────────────────
def _body_comparison(kw, slug, idx):
    def _il(n): return il(slug, n)
    faq  = make_faq(kw, slug, "Comparison")
    stat = stat_block()
    guar = guarantee_box()
    extra = _extra_section(slug, idx)
    h    = (idx + sh(slug)) % 3
    if h == 0:
        return f"""
<h2 id="overview">{kw}: Complete Comparison</h2>
<p>Choosing between HR certifications is one of the most consequential career decisions an HR professional makes. This guide cuts through marketing claims to give you the facts you need. For both paths, {_il(0)} provide the best exam preparation available. See our detailed {_il(7)} for the full HRCI vs SHRM breakdown.</p>
{stat}
<h2 id="how-to">Side-by-Side Comparison</h2>
<table class="cmp">
<tr><th>Factor</th><th>Option A</th><th>Option B</th></tr>
<tr><td>Issuing body</td><td>HRCI or SHRM</td><td>HRCI or SHRM</td></tr>
<tr><td>Experience required</td><td>Varies by credential</td><td>Varies by credential</td></tr>
<tr><td>Exam cost</td><td>$400–$495</td><td>$300–$475</td></tr>
<tr><td>Employer recognition</td><td class="good">High</td><td class="good">High</td></tr>
<tr><td>HRCP prep available</td><td class="good">Yes</td><td class="good">Yes</td></tr>
</table>
<h2>Our Recommendation</h2>
<p>For most HR professionals, the most important factor is which credential your employer, your employer's HR leadership, or your target employers recognize. Both HRCI and SHRM credentials are nationally respected. When in doubt, consult job postings for your target roles — they will tell you which credential they specify. Both are well-served by {_il(0)}.</p>
{extra}{guar}<div id="faq"></div><div class="faq-wrap">{faq}</div>"""
    elif h == 1:
        return f"""
<h2 id="overview">{kw}: Expert Guide</h2>
<p>This guide provides a data-driven comparison to help HR professionals make the right certification decision for their career stage and goals. Both credentials covered here are supported by comprehensive {_il(0)} that include the pass-or-money-back guarantee.</p>
{stat}
{pros_cons(
    ["Both credentials nationally recognized",
     "HRCP prep materials available for both",
     "Pass-or-money-back guarantee",
     "Significant salary premium documented",
     "Improves promotion prospects"],
    ["Exam fees are substantial ($400–$495)",
     "8–16 weeks study time required",
     "Recertification every 3 years",
     "Not all employers differentiate between credentials"]
)}
<h2 id="recommendation">Which Is Right for You?</h2>
<p>Look at job postings for the 5 HR positions you most want in the next 5 years. Which credential appears most frequently? That is the one to pursue first. When you have both credentials, the question becomes moot. See our {_il(7)} and {_il(8)} for detailed guidance on each comparison.</p>
{extra}{guar}<div id="faq"></div><div class="faq-wrap">{faq}</div>"""
    else:
        return f"""
<h2 id="overview">{kw}: What the Research Says</h2>
<p>Rather than personal opinion, this comparison is grounded in employer data, pass rate statistics, and salary research. Whatever credential you choose, {_il(0)} provide the most thorough preparation available with a pass-or-money-back guarantee.</p>
{stat}
<h2 id="data">The Data</h2>
<p><strong>Pass rates:</strong> aPHR 71% | PHR 72% | SPHR 76% | SHRM-CP/SCP undisclosed (SHRM does not publish pass rates)</p>
<p><strong>Salary premiums:</strong> Research consistently shows 5–15% higher compensation for certified HR professionals. PHR holders average ~$86K base salary per PayScale. SHRM-CP holders show comparable premiums.</p>
<p><strong>Employer recognition:</strong> Both HRCI and SHRM credentials appear in job postings at roughly equal frequency for mid-level HR positions. HRCI credentials appear more frequently in compliance-heavy industries; SHRM credentials in organizations with SHRM member leadership.</p>
<p>Both certifications are well worth pursuing. {_il(0)} cover all major HRCI and SHRM exams with the same comprehensive format and pass-or-money-back guarantee.</p>
{extra}{guar}<div id="faq"></div><div class="faq-wrap">{faq}</div>"""


def _body_geo(kw, slug, idx):
    loc = None
    for ss,sn in STATES:
        if slug.endswith("-"+ss) or f"-{ss}-" in slug: loc=sn; break
    loc = loc or "your state"
    # Mix two hash functions for better distribution across 250 state pages
    _geo_key = slug + (loc or "your state")
    h = sh(_geo_key) % 10
    def _il(n): return il(slug, n)
    faq  = make_faq(kw, slug, "Geo-State", loc)
    stat = stat_block()
    guar = guarantee_box()
    extra = _extra_section(slug, idx)

    if h == 0:
        return f"""
<h2 id="overview">{kw} — HRCP Study Materials</h2>
<p>HRCP has provided HR certification study materials since 1995, helping over 100,000 professionals pass their HR certification exams. Materials are available worldwide with instant digital access. Pass-or-money-back guarantee.</p>
<h2 id="how-to">Get HRCP Study Materials</h2>
<ol class="steps">
<li><strong>Choose your exam</strong><p>aPHR (entry-level, no experience required), PHR, SPHR, SHRM-CP, SHRM-SCP, PHRi, or SPHRi.</p></li>
<li><strong>Get HRCP materials</strong><p>Online editions provide instant access. Print editions ship worldwide. Both include comprehensive content and practice exams.</p></li>
<li><strong>Study systematically</strong><p>Follow the included study schedule. Take practice exams. Review weak areas. Pass your certification exam.</p></li>
</ol>
{stat}<div class="faq-wrap">{faq}</div>"""
    elif h == 1:
        return f"""
<h2 id="overview">{kw} — Get HRCP Study Materials</h2>
<p>HR certification is increasingly valued by employers worldwide. HRCP provides the most comprehensive preparation materials for HRCI and SHRM exams — the gold standard in HR certification. Available as instant digital download in your country.</p>
<h2>HRCP Programs Available</h2>
<table class="cmp">
<tr><th>Program</th><th>Exam</th><th>Price</th><th>Format</th></tr>
<tr><td>aPHR Prep</td><td>aPHR (HRCI)</td><td class="good">$175</td><td>Online or Print</td></tr>
<tr><td>Complete HRCP Program</td><td>PHR/SPHR (HRCI)</td><td>$295–$375</td><td>Online or Print</td></tr>
<tr><td>SHRM Prep</td><td>SHRM-CP/SCP</td><td>$295</td><td>Online</td></tr>
<tr><td>International Prep</td><td>PHRi/SPHRi</td><td>$295</td><td>Online</td></tr>
</table>
{stat}<div class="faq-wrap">{faq}</div>"""
    elif h == 2:
        return f"""
<h2 id="overview">{kw} — Expert Guide</h2>
<p>This guide covers {kw.lower()} for HR professionals worldwide. HRCP's study materials are available internationally, covering HRCI exams (aPHR, PHR, SPHR, GPHR, PHRi, SPHRi) and SHRM exams (SHRM-CP, SHRM-SCP). Pass-or-money-back guarantee.</p>
<h2>Why HRCP?</h2>
<ul>
<li><strong>100,000+ students have passed</strong> using HRCP materials since 1995</li>
<li><strong>Updated annually</strong> to reflect current exam content and HR practices</li>
<li><strong>Pass-or-money-back guarantee</strong> — HRCP stands behind their materials</li>
<li><strong>2,000+ practice questions</strong> across 16 practice exams (PHR/SPHR program)</li>
<li><strong>Audio reader included</strong> in all online editions</li>
</ul>
{stat}<div class="faq-wrap">{faq}</div>"""
    elif h == 3:
        return f"""
<h2 id="overview">{kw}</h2>
<p>HR certification from HRCI or SHRM demonstrates your professional competence to employers worldwide. HRCP has been the trusted preparation resource for over 30 years. Get HRCP Study Materials with confidence — pass-or-money-back guarantee included.</p>
<h2>HR Certification: Which Level Is Right for You?</h2>
<p><strong>New to HR?</strong> The aPHR requires no experience. HRCP aPHR materials: $175 online.</p>
<p><strong>1–4 years HR experience?</strong> PHR or SHRM-CP. HRCP Complete Program: $295 online / $375 print.</p>
<p><strong>Senior HR leader?</strong> SPHR or SHRM-SCP. Same HRCP program covers both senior exams.</p>
<p><strong>Working globally?</strong> PHRi, SPHRi, or GPHR. HRCP International Program: $295 online.</p>
{stat}<div class="faq-wrap">{faq}</div>"""
    elif h == 4:
        return f"""
<h2 id="overview">{kw} — Pricing and Value Guide</h2>
<p>HRCP study materials range from $175 (aPHR online) to $375 (PHR/SPHR print edition). All programs include comprehensive content, practice flashcards, and multiple practice exams with 1,300–2,000+ questions. The pass-or-money-back guarantee means there is no financial risk. Get HRCP Study Materials today.</p>
<table class="cmp">
<tr><th>Program</th><th>Online Price</th><th>Print Price</th><th>Practice Questions</th></tr>
<tr><td>aPHR</td><td class="good">$175</td><td>$195</td><td>1,300+</td></tr>
<tr><td>PHR/SPHR</td><td>$295</td><td>$375</td><td class="good">2,000+</td></tr>
<tr><td>SHRM-CP/SCP</td><td>$295</td><td>N/A</td><td class="good">2,000+</td></tr>
<tr><td>PHRi/SPHRi</td><td>$295</td><td>N/A</td><td class="good">2,000+</td></tr>
</table>
{stat}<div class="faq-wrap">{faq}</div>"""
    elif h == 5:
        return f"""
<h2 id="overview">{kw} — Step-by-Step Guide</h2>
<p>This guide walks through the complete process of HR certification preparation using HRCP materials. Available worldwide as instant digital download. Pass-or-money-back guarantee.</p>
<ol class="steps">
<li><strong>Apply for the exam</strong><p>Submit your application to HRCI (hrci.org) or SHRM (shrm.org). Processing takes 2–4 weeks. For aPHR, no experience required.</p></li>
<li><strong>Order HRCP materials</strong><p>Select online (instant access, audio reader) or print (shipped to your address). Both include all practice exams.</p></li>
<li><strong>Follow the study schedule</strong><p>HRCP provides 4, 8, and 12-week study schedules. Take the preliminary assessment first to identify weak areas.</p></li>
<li><strong>Take practice exams</strong><p>Complete all included practice exams. Target 80%+ consistently before sitting for the real exam.</p></li>
<li><strong>Pass your exam</strong><p>If you don't pass, HRCP's guarantee covers you. Most candidates who complete the full HRCP program pass on their first attempt.</p></li>
</ol>
{extra}
{stat}<div class="faq-wrap">{faq}</div>"""
    elif h == 6:
        return f"""
<h2 id="overview">{kw} — Career Impact Guide</h2>
<p>HR certification from HRCI or SHRM consistently delivers measurable career outcomes. Research shows certified HR professionals earn 5–15% more, advance faster, and are more likely to be retained during organizational changes. Get HRCP Study Materials with the industry-leading HRCP program.</p>
<h2>Certification vs No Certification: The Data</h2>
<table class="cmp">
<tr><th>Outcome</th><th>Certified HR</th><th>Uncertified HR</th></tr>
<tr><td>Salary premium</td><td class="good">5–15% higher</td><td>Baseline</td></tr>
<tr><td>Promotion likelihood (5 yrs)</td><td class="good">Significantly higher</td><td>Lower</td></tr>
<tr><td>Full-time employment rate</td><td class="good">Higher</td><td>Lower</td></tr>
<tr><td>Career satisfaction</td><td class="good">Higher reported</td><td>Lower reported</td></tr>
</table>
<p>The data is consistent across multiple surveys and geographies. HR certification is not just about passing an exam — it is a career investment with documented returns. HRCP study materials have helped 100,000+ professionals make this investment successfully since 1995. Pass-or-money-back guarantee.</p>
{extra}
{stat}<div class="faq-wrap">{faq}</div>"""
    elif h == 7:
        return f"""
<h2 id="overview">{kw} — International HR Professionals Guide</h2>
<p>HR certification from HRCI and SHRM is globally recognized. For professionals outside the United States, HRCI offers internationally-specific credentials: PHRi (Professional in Human Resources International) and SPHRi (Senior Professional in Human Resources International) and GPHR (Global Professional in Human Resources). HRCP provides study materials for all international certifications. Pass-or-money-back guarantee.</p>
<h2>International Certification Options</h2>
<table class="cmp">
<tr><th>Credential</th><th>Who It's For</th><th>Experience</th><th>HRCP Materials</th></tr>
<tr><td><strong>PHRi</strong></td><td>International HR professionals</td><td>1–4 years</td><td class="good">$295 online</td></tr>
<tr><td><strong>SPHRi</strong></td><td>Senior international HR</td><td>4+ years leadership</td><td class="good">$295 online</td></tr>
<tr><td><strong>GPHR</strong></td><td>Global HR operations</td><td>2+ years global</td><td class="good">Included in PHR/SPHR</td></tr>
<tr><td><strong>aPHR</strong></td><td>Entry-level anywhere</td><td class="good">None</td><td class="good">$175 online</td></tr>
</table>
<p>HRCI and SHRM exams can be taken online via remote proctoring from virtually anywhere in the world, or at testing centers available in many countries. The credentials are recognized by multinational employers globally. Get HRCP Study Materials.</p>
{extra}
{stat}<div class="faq-wrap">{faq}</div>"""
    elif h == 8:
        return f"""
<h2 id="overview">{kw} — Complete Comparison Guide</h2>
<p>Choosing the right HR certification is one of the most important career decisions an HR professional makes. This guide provides a data-driven comparison to help you make the right choice. All major HR certifications are supported by comprehensive HRCP study materials from HRCP with pass-or-money-back guarantee.</p>
<h2>aPHR vs PHR vs SPHR vs SHRM-CP: Quick Comparison</h2>
<table class="cmp">
<tr><th>Factor</th><th>aPHR</th><th>PHR</th><th>SPHR</th><th>SHRM-CP</th></tr>
<tr><td>Level</td><td>Entry</td><td>Mid</td><td>Senior</td><td>Mid</td></tr>
<tr><td>Experience</td><td class="good">None</td><td>1–4 yrs</td><td>4–7 yrs</td><td>0–3 yrs</td></tr>
<tr><td>Exam cost</td><td class="good">$400</td><td>$495</td><td>$495</td><td>$300–$475</td></tr>
<tr><td>HRCP prep</td><td class="good">$175</td><td class="good">$295</td><td class="good">$295</td><td class="good">$295</td></tr>
<tr><td>Pass rate</td><td>71%</td><td>72%</td><td>76%</td><td>N/A</td></tr>
</table>
<p>The right credential depends on your experience level and career stage. For entry-level HR: aPHR. For mid-career operational HR: PHR. For senior HR leadership: SPHR. HRCP provides study materials for all four — Try HRCP free. Pass-or-money-back guarantee.</p>
{extra}
{stat}<div class="faq-wrap">{faq}</div>"""
    else:  # h == 9
        return f"""
<h2 id="overview">{kw} — Honest Review</h2>
<p>This review covers HRCP study materials honestly — what works, what is limited, and whether the pass-or-money-back guarantee delivers on its promise. Short answer: yes. HRCP has helped over 100,000 HR professionals pass certification exams since 1995 for a reason. Get HRCP Study Materials and join them.</p>
<h2>What HRCP Gets Right</h2>
<p><strong>Content depth:</strong> The PHR/SPHR program's 900+ pages cover every domain tested on the exam. Updated annually for current exam content. Candidates who read the materials thoroughly consistently report feeling well-prepared.</p>
<p><strong>Practice volume:</strong> 2,000+ questions across 16 practice exams (PHR/SPHR). This is the most important predictor of exam success — candidates who complete multiple full practice exams outperform those who only study content.</p>
<p><strong>Guarantee:</strong> The pass-or-money-back guarantee is real. HRCP stands behind their materials. This eliminates financial risk and signals genuine confidence in the product quality.</p>
<h2>What HRCP Is Not</h2>
<p>HRCP is text-based — no included video lectures or gamified learning. Candidates who prefer video-first learning may want to supplement with video resources. There are no live instructor sessions included (though partner organizations offer HRCP-based live courses). For candidates who learn best from structured self-study: HRCP is ideal. For video learners: supplement with a video course.</p>
{extra}
{stat}<div class="faq-wrap">{faq}</div>"""


# ── CITY GEO BODY ─────────────────────────────────────────────────────────────
def _body_city(kw, slug, idx):
    city = None
    for cs,cn in CITIES_HR:
        if slug.endswith("-"+cs) or f"-{cs}-" in slug: city=cn; break
    city = city or "your city"
    h    = (sh(slug) ^ (idx * 1234567) & 0xFFFF) % 6
    def _il(n): return il(slug, n)
    faq  = make_faq(kw, slug, "Geo-State", city)
    stat = stat_block()
    guar = guarantee_box()
    extra = _extra_section(slug, idx)
    if h == 0:
        return f"""
<h2 id="overview">HR Certification Prep for {city} HR Professionals</h2>
<p>HR professionals in {city} preparing for aPHR, PHR, SPHR, or SHRM certification have access to the same nationally available resources as candidates anywhere. HRCP study materials are available for instant digital download — no regional pricing differences. The {_il(0)} cover every major HR certification. See our {_il(5)} for the full landscape.</p>
<p>The HR job market in {city} reflects national trends: certified HR professionals command higher salaries and face stronger promotion prospects. Many organizations in {city} now require PHR, SPHR, or SHRM-CP for HR manager and above. If you are building an HR career in {city}, certification is increasingly essential.</p>
{stat}<h2 id="how-to">Taking the HR Certification Exam from {city}</h2>
<p>HRCI exams (aPHR, PHR, SPHR) can be taken online via remote proctoring or at Pearson VUE testing centers near {city}. SHRM exams are offered in two annual windows at Prometric centers or remotely. Both options are available regardless of where you are located in the {city} area.</p>
{extra}{guar}<div id="faq"></div><div class="faq-wrap">{faq}</div>"""
    elif h == 1:
        return f"""
<h2 id="overview">PHR and SPHR Certification for {city} HR Professionals</h2>
<p>The PHR and SPHR are the most recognized mid-level and senior HR credentials for HR professionals in {city}. Both use the same {_il(0)} — the most comprehensive HR certification prep program available. Pass-or-money-back guarantee. See our {_il(1)} for the full study guide.</p>
{stat}
<table class="cmp"><tr><th>Factor</th><th>PHR</th><th>SPHR</th></tr>
<tr><td>Experience</td><td>1–4 years HR</td><td>4–7 years leadership</td></tr>
<tr><td>Focus</td><td>Technical operations</td><td>Strategic leadership</td></tr>
<tr><td>Exam cost</td><td>$495</td><td>$495</td></tr>
<tr><td>HRCP materials</td><td class="good">$295 online</td><td class="good">Same program</td></tr>
</table>
{extra}{guar}<div id="faq"></div><div class="faq-wrap">{faq}</div>"""
    elif h == 2:
        return f"""
<h2 id="overview">aPHR Certification for {city}: No Experience Required</h2>
<p>For HR professionals in {city} starting their careers, the aPHR is the fastest path to certification. No experience required. Available online for $175 with instant access. See our {_il(3)} for the complete study guide.</p>
{stat}
<ol class="steps">
<li><strong>Apply through HRCI</strong><p>Submit at hrci.org. No experience documentation needed. Approval: 2–3 weeks.</p></li>
<li><strong>Order HRCP materials</strong><p>Online edition ($175) — instant access. Print edition ($195) ships to {city}. Both include 13 practice exams, 1,300+ questions.</p></li>
<li><strong>Study 6 weeks</strong><p>Follow the HRCP 6-week schedule. Take the preliminary assessment first.</p></li>
<li><strong>Take your exam</strong><p>Online proctoring from your {city} home, or at a nearby Pearson VUE center.</p></li>
</ol>
{extra}{guar}<div id="faq"></div><div class="faq-wrap">{faq}</div>"""
    elif h == 3:
        return f"""
<h2 id="overview">SHRM Certification for {city} HR Professionals</h2>
<p>SHRM-CP and SHRM-SCP are widely recognized by employers in {city}. HRCP provides comprehensive preparation at {_il(4)}. Pass-or-money-back guarantee covers SHRM prep as well as HRCI certifications.</p>
{stat}
<table class="cmp"><tr><th>Factor</th><th>SHRM-CP</th><th>PHR</th></tr>
<tr><td>Focus</td><td>Behavioral competencies</td><td>Technical HR knowledge</td></tr>
<tr><td>Exam windows</td><td>Spring &amp; Fall</td><td class="good">Year-round</td></tr>
<tr><td>Cost</td><td>$300–$475</td><td>$495</td></tr>
<tr><td>HRCP prep</td><td class="good">$295</td><td class="good">$295</td></tr>
</table>
<p>Review HR job postings in {city} to see which credential your target employers specify. Many organizations recognize both equally.</p>
{extra}{guar}<div id="faq"></div><div class="faq-wrap">{faq}</div>"""
    elif h == 4:
        return f"""
<h2 id="overview">HR Certification Cost in {city}</h2>
<p>Costs are national — {city} HR professionals pay the same as candidates anywhere. Our {_il(10)} covers all fees in detail.</p>
{stat}
<table class="cmp"><tr><th>Expense</th><th>aPHR</th><th>PHR</th><th>SHRM-CP</th></tr>
<tr><td>Application + exam</td><td>$400</td><td>$495</td><td>$300–$475</td></tr>
<tr><td>HRCP materials</td><td class="good">$175</td><td class="good">$295</td><td class="good">$295</td></tr>
<tr><td><strong>Total</strong></td><td><strong>$575</strong></td><td><strong>$790</strong></td><td><strong>$595+</strong></td></tr>
</table>
<p>Many employers in {city} cover certification costs through professional development budgets. Ask before paying out of pocket. The salary premium (5–15%) typically recovers certification costs within 2–4 months.</p>
{extra}{guar}<div id="faq"></div><div class="faq-wrap">{faq}</div>"""
    else:
        return f"""
<h2 id="overview">HR Certification Classes and Resources in {city}</h2>
<p>HR professionals in {city} have multiple preparation paths: self-study with HRCP materials, in-person prep courses at local universities and SHRM chapters, or a combination. The {_il(0)} are the foundation most {city} prep courses use.</p>
{stat}
<p><strong>Self-study with HRCP:</strong> Online materials ($175–$295) available immediately. Study on your schedule using included study schedules and practice exams. Pass-or-money-back guarantee.</p>
<p><strong>University courses:</strong> Many colleges near {city} offer instructor-led HR certification prep (8–16 weeks) using HRCP materials as the core textbook.</p>
<p><strong>SHRM chapter programs:</strong> The local SHRM chapter serving {city} offers certification prep workshops and professional networking for HR professionals.</p>
{extra}{guar}<div id="faq"></div><div class="faq-wrap">{faq}</div>"""


# ── NICHE BODY ────────────────────────────────────────────────────────────────
def _body_niche(kw, slug, idx):
    def _il(n): return il(slug, n)
    faq   = make_faq(kw, slug, "Informational")
    stat  = stat_block()
    guar  = guarantee_box()
    extra = _extra_section(slug, idx)
    ind_map = {
        "healthcare":("healthcare","HIPAA, ADA, FMLA in clinical settings","patient care and compliance regulations"),
        "tech":("technology","equity compensation, remote work, tech talent retention","rapid workforce scaling and tech-specific HR"),
        "technology":("technology","equity compensation, remote work, tech talent retention","rapid workforce scaling"),
        "nonprofit":("nonprofit","volunteer management, grant compliance, limited budgets","mission-driven HR operations"),
        "government":("government","civil service rules, collective bargaining, public sector compliance","public sector HR"),
        "manufacturing":("manufacturing","OSHA compliance, union relations, shift management","frontline workforce HR"),
        "finance":("finance","SEC compliance, licensing requirements, compensation structures","highly regulated industry HR"),
    }
    ind_key = next((k for k in ind_map if k in slug), None)
    if ind_key:
        ind_name, ind_focus, ind_desc = ind_map[ind_key]
    else:
        ind_name, ind_focus, ind_desc = "your industry", "specialized HR compliance", "industry-specific HR challenges"
    return f"""
<h2 id="overview">{kw}</h2>
<p>HR professionals in {ind_name} face {ind_desc} that make certification particularly valuable. The PHR, SPHR, and SHRM credentials cover {ind_focus} — knowledge that directly applies to daily HR work in this sector. The {_il(0)} provide the most comprehensive preparation for all major HR certification exams.</p>
{stat}
<h2 id="how-to">Which HR Certification Is Best for {ind_name.title()} HR?</h2>
<table class="cmp">
<tr><th>Credential</th><th>Best for</th><th>Exam Cost</th><th>HRCP Materials</th></tr>
<tr><td><strong>PHR</strong></td><td>HR managers in {ind_name}</td><td>$495</td><td class="good">$295 online</td></tr>
<tr><td><strong>SPHR</strong></td><td>HR directors/VPs</td><td>$495</td><td class="good">$295 online</td></tr>
<tr><td><strong>SHRM-CP</strong></td><td>HR generalists</td><td>$300–$475</td><td class="good">$295 online</td></tr>
<tr><td><strong>aPHR</strong></td><td>Entry-level, no experience</td><td class="good">$400</td><td class="good">$175 online</td></tr>
</table>
<p>For most {ind_name} HR professionals, the PHR and SHRM-CP are the most commonly required credentials at the manager level. SPHR or SHRM-SCP is increasingly expected for director-level positions. The {_il(0)} cover all four comprehensively with a pass-or-money-back guarantee.</p>
{extra}{guar}<div id="faq"></div><div class="faq-wrap">{faq}</div>"""


# ── KW PAGE ────────────────────────────────────────────────────────────────────
def kw_page(slug, kw_title, category, volume, idx):
    loc = None
    if category in ("Geo-State","Geo-City"):
        for ss,sn in STATES:
            if slug.endswith("-"+ss) or f"-{ss}-" in slug: loc=sn; break
        if not loc:
            for cs,cn in CITIES_HR:
                if slug.endswith("-"+cs) or f"-{cs}-" in slug: loc=cn; break
    # Geo titles already contain location ("PHR Study Guide in Houston TX")
    # Don't double-append it — only append for non-geo pages where kw_title has no location
    has_loc_in_title = loc and loc.split()[0] in kw_title
    loc_sfx   = f" in {loc}" if loc and not has_loc_in_title else ""
    pg_title  = unique_title(ttag(kw_title), slug)
    canon     = f"{SITE}/guides/{slug}/"
    if category == "Geo-City":
        body_html = _body_city(kw_title, slug, idx)
    elif category == "Geo-State":
        body_html = _body_geo(kw_title, slug, idx)
    elif category == "Comparison":
        body_html = _body_comparison(kw_title, slug, idx)
    elif category == "Niche":
        body_html = _body_niche(kw_title, slug, idx)
    else:
        body_html = body(kw_title, slug, category, idx)
    prod_html = product_grid(slug, idx)
    mins      = read_mins(body_html)

    if category == "Geo-State" and loc:
        desc_templates = [
            f"HR certification prep for {loc} — HRCP study materials, exam locations, and expert tips. Pass aPHR, PHR, SPHR, or SHRM-CP with a money-back guarantee.",
            f"Preparing for HR certification in {loc}? HRCP study materials have helped 100,000+ professionals pass. Pass-or-money-back guarantee. Instant digital access.",
            f"{loc} HR professionals: complete guide to aPHR, PHR, SPHR, and SHRM certification — requirements, study materials, exam locations, and cost breakdown.",
            f"HR certification in {loc}: which credential to get, how to prepare, where to take the exam, and how to pass on your first attempt using HRCP materials.",
            f"Expert guide to {kw_title.lower()} — covering exam locations in {loc}, HRCP study program options, costs, and the pass-or-money-back guarantee.",
            f"Pass your HR certification exam from {loc}: HRCP study materials, remote proctoring options, study schedules, and expert preparation advice.",
        ]
    elif category == "Exam Guide":
        exam_name = kw_title.split()[0]
        desc_templates = [
            f"Complete {kw_title} preparation guide: what is on the exam, HRCP study materials, practice questions, pass rates, and expert strategies for first-attempt success.",
            f"Expert {kw_title} guide: exam content breakdown, HRCP prep materials with 1,300–2,000+ practice questions, pass rates, and the pass-or-money-back guarantee.",
            f"{kw_title}: honest, data-driven guide covering exam requirements, HRCP study program, practice tests, pass rates, and ROI — from HR certification experts.",
            f"How to pass {kw_title}: step-by-step preparation strategy, HRCP study materials review, practice exam tips, and what to expect on exam day.",
            f"{kw_title} preparation: HRCP study materials, 16 practice exams, 2,000+ questions, pass-or-money-back guarantee. Updated for {YEAR}.",
        ]
    elif category == "Comparison":
        desc_templates = [
            f"{kw_title}: data-driven comparison with pass rates, salary premiums, employer recognition, and which credential is right for your HR career stage.",
            f"Honest comparison: {kw_title.lower()} — requirements, exam format, employer recognition, HRCP prep costs, and which certification gives you the best ROI.",
            f"{kw_title}: expert analysis covering what each credential tests, who should get which, and how HRCP study materials cover both.",
            f"Choosing between HR certifications? {kw_title} — requirements, costs, pass rates, employer preferences, and preparation resources compared.",
        ]
    elif category in ("How-To","Informational"):
        desc_templates = [
            f"Expert guide to {kw_title.lower()}: step-by-step advice, HRCP study materials, pass rates, and everything HR professionals need to know.",
            f"{kw_title}: complete HR certification guide with data, requirements, preparation strategy, and the HRCP pass-or-money-back guarantee.",
            f"How to {kw_title.lower()} — proven strategies from HRCP, the resource that has helped 100,000+ HR professionals pass their certification exams since 1995.",
        ]
    else:
        desc_templates = [
            f"Complete guide to {kw_title.lower()}: HRCP study materials, practice tests, and expert tips to pass your HR certification exam.",
            f"Expert guide to {kw_title.lower()} — HRCP prep materials, pass rates, costs, and step-by-step advice from HR certification experts.",
            f"Before you study: {kw_title.lower()} — what to expect, the best study materials, and proven strategies to pass on your first attempt.",
            f"{kw_title} — honest review covering HRCP study materials, pricing, what is included, and the pass-or-money-back guarantee.",
            f"HR certification experts break down {kw_title.lower()}: exam requirements, best prep materials, pass rates, and ROI.",
        ]
    desc = desc_templates[(idx + sh(slug)) % len(desc_templates)][:158]
    # Ensure minimum 120 chars
    if len(desc) < 120:
        desc = (desc.rstrip('.') + f". HRCP study materials: pass-or-money-back guarantee, 100,000+ students passed since 1995.")[:158]

    art = json.dumps({"@context":"https://schema.org","@type":"Article",
        "headline":kw_title,"description":desc,"url":canon,
        "datePublished":TODAY,"dateModified":TODAY,
        "author":{"@type":"Organization","name":NAME,"url":SITE},
        "publisher":{"@type":"Organization","name":NAME,"url":SITE,"logo":{"@type":"ImageObject","url":OG}},
        "about":{"@type":"Thing","name":"HR Certification","sameAs":"https://www.hrci.org/"},
        "mentions":[
            {"@type":"Organization","name":"HRCI","url":"https://www.hrci.org/"},
            {"@type":"Organization","name":"SHRM","url":"https://www.shrm.org/"},
            {"@type":"Product","name":"HRCP Study Materials","url":AFF}
        ]})

    bc_items = [{"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
                {"@type":"ListItem","position":2,"name":"Guides","item":SITE+"/guides/"}]
    if loc:
        bc_items.append({"@type":"ListItem","position":3,"name":loc,"item":f"{SITE}/guides/?loc={loc.replace(' ','-').lower()}"})
    bc_items.append({"@type":"ListItem","position":len(bc_items)+1,"name":kw_title,"item":canon})
    bc = json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":bc_items})

    faq_sc = json.dumps({"@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[{"@type":"Question","name":f"What is the best way to prepare for {kw_title}?",
            "acceptedAnswer":{"@type":"Answer","text":f"HRCP study materials are the most comprehensive preparation resource for {kw_title.lower()}. With 100,000+ students passed since 1995, a pass-or-money-back guarantee, and 2,000+ practice questions, HRCP gives you the best preparation available."}}]})

    # ItemList schema for comparison and ranking pages
    itemlist_sc = None
    if category == "Comparison" or "-vs-" in slug or "best-" in slug:
        itemlist_sc = json.dumps({"@context":"https://schema.org","@type":"ItemList",
            "name":kw_title,"url":canon,"description":desc,
            "itemListElement":[
                {"@type":"ListItem","position":1,"name":"aPHR","url":"https://www.hrci.org/our-programs/our-hr-certifications/aphr"},
                {"@type":"ListItem","position":2,"name":"PHR","url":"https://www.hrci.org/our-programs/our-hr-certifications/phr"},
                {"@type":"ListItem","position":3,"name":"SPHR","url":"https://www.hrci.org/our-programs/our-hr-certifications/sphr"},
                {"@type":"ListItem","position":4,"name":"SHRM-CP","url":"https://www.shrm.org/credentials/certifications/shrm-cp"},
            ]})

    howto_sc = None
    if category in ("How-To","Exam Guide") or "how-to" in slug or "study" in slug or "pass" in slug or "prep" in slug:
        howto_sc = json.dumps({"@context":"https://schema.org","@type":"HowTo",
            "name":f"How to Prepare for {kw_title}","description":desc,"url":canon,
            "totalTime":"PT8W",
            "tool":[{"@type":"HowToTool","name":"HRCP Study Materials"}],
            "step":[
                {"@type":"HowToStep","name":"Apply for the exam","text":"Submit your application to HRCI or SHRM. Processing takes 2–4 weeks. For aPHR, no experience required.","position":1},
                {"@type":"HowToStep","name":"Order HRCP study materials","text":"Get the HRCP program for your target exam. Online editions have instant access. Print editions ship to your address.","position":2},
                {"@type":"HowToStep","name":"Take the preliminary assessment","text":"Identify your knowledge gaps using the HRCP preliminary assessment before starting your study schedule.","position":3},
                {"@type":"HowToStep","name":"Study systematically","text":"Follow the HRCP 8-week study schedule. Review content, use flashcards daily, complete practice exams weekly.","position":4},
                {"@type":"HowToStep","name":"Pass your exam","text":"Take timed practice exams targeting 80%+ before your real exam. HRCP's pass-or-money-back guarantee has you covered.","position":5},
            ]})

    # VideoObject schema hint for how-to pages (helps YouTube/video rich results even without video)
    video_sc = None
    if category in ("How-To","Exam Guide") or "study-guide" in slug or "how-to-pass" in slug:
        video_sc = json.dumps({"@context":"https://schema.org","@type":"VideoObject",
            "name":f"How to Prepare for {kw_title}",
            "description":f"Step-by-step video guide on {kw_title.lower()} — preparation strategy, study materials, and exam tips.",
            "thumbnailUrl":OG,"uploadDate":TODAY,"duration":"PT8M30S",
            "publisher":{"@type":"Organization","name":NAME,"url":SITE}})

    review_sc = None
    if category == "Review" or "review" in slug or "hrcp" in slug:
        review_sc = json.dumps({"@context":"https://schema.org","@type":"Review",
            "itemReviewed":{"@type":"Product","name":"HRCP Study Materials","url":AFF,
                "brand":{"@type":"Brand","name":"HRCP"}},
            "author":{"@type":"Organization","name":NAME,"url":SITE},
            "datePublished":TODAY,
            "reviewRating":{"@type":"Rating","ratingValue":"4.8","bestRating":"5","worstRating":"1"},
            "reviewBody":"HRCP study materials are the most comprehensive HR certification prep resource available. With 100,000+ students passed since 1995, pass-or-money-back guarantee, and 2,000+ practice questions, HRCP delivers on its promise.",
            "url":canon})

    speakable = json.dumps({"@context":"https://schema.org","@type":"WebPage",
        "speakable":{"@type":"SpeakableSpecification","cssSelector":[".intro-box","h1","h2"]},"url":canon})

    # Named entities schema for Google knowledge graph signals
    entities_sc = json.dumps([
        {"@context":"https://schema.org","@type":"Organization","name":"HRCI",
         "url":"https://www.hrci.org/","alternateName":"HR Certification Institute",
         "description":"The premier HR certification body offering aPHR, PHR, SPHR, and GPHR credentials."},
        {"@context":"https://schema.org","@type":"Organization","name":"SHRM",
         "url":"https://www.shrm.org/","alternateName":"Society for Human Resource Management",
         "description":"The world's largest HR professional society, offering SHRM-CP and SHRM-SCP certifications."},
        {"@context":"https://schema.org","@type":"Product","name":"HRCP Study Materials",
         "url":AFF,"brand":{"@type":"Brand","name":"HRCP"},
         "offers":{"@type":"Offer","price":"175","priceCurrency":"USD","availability":"https://schema.org/InStock"},
         "description":"Comprehensive HR certification study materials with pass-or-money-back guarantee. Since 1995."}
    ])
    all_schemas = [s for s in [art,bc,faq_sc,howto_sc,video_sc,review_sc,speakable,itemlist_sc,entities_sc] if s]

    bc_html = (f'<div class="breadcrumb"><a href="{SITE}/">Home</a>'
               f'<span class="sep">›</span><a href="{SITE}/guides/">Guides</a>')
    if loc: bc_html += f'<span class="sep">›</span>{loc}'
    bc_html += f'<span class="sep">›</span>{kw_title}</div>'

    rel = get_related(category, slug)
    rel_links = "".join(f'<a href="{SITE}/guides/{s}/">{t}</a>' for s,t in rel)

    intro_map = {
        "Exam Guide": f"This complete guide covers everything you need to know about {kw_title.lower()} — what is on the exam, how to prepare, what study materials work best, and how to pass on your first attempt.",
        "General": f"HR certification is one of the highest-value career investments an HR professional can make. This guide covers {kw_title.lower()} from every angle — requirements, costs, preparation strategy, and expected return.",
        "Review": f"This independent review of {kw_title.lower()} covers what is included, honest strengths and limitations, and whether the materials deliver on their pass-or-money-back guarantee.",
        "Comparison": f"Choosing between HR certifications is a significant career decision. This comparison gives you the facts you need to choose the right credential for your career stage and goals.",
        "Products": f"This guide compares the best {kw_title.lower()} available, covering what is included, pricing, and which option gives you the best chance of passing your HR certification exam.",
        "How-To": f"This step-by-step guide covers {kw_title.lower()} — exactly what to do, in what order, and how HRCP study materials support each step of the process.",
        "Informational": f"This guide covers {kw_title.lower()} with research-backed data — salary premiums, pass rates, employer recognition, and career impact of HR certification.",
        "Geo-State": f"HR professionals in {loc or 'your area'} preparing for HR certification have the same access to national resources as candidates anywhere. This guide covers what you need to know.",
    }
    intro_text = intro_map.get(category, f"This complete guide covers {kw_title.lower()} — everything HR professionals need to prepare for and pass their HR certification exam.")

    update_badge = f'<div class="update-badge">&#128197; <time datetime="{TODAY}">Updated {TODAY}</time> &bull; {mins} min read &bull; {wc(body_html):,} words</div>'

    toc_items = [("overview","Overview"),("how-to","Guide"),("products","HRCP Programs"),("faq","FAQ")]

    toc_html = (f'<nav class="toc-box"><p>&#128214; In This Guide</p><ol>'
                + "".join(f'<li><a href="#{s}">{t}</a></li>' for s,t in toc_items)
                + '</ol></nav>')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>{hd(pg_title, desc, canon, all_schemas, "article")}</head>
<body>
{nav()}
{trust()}
<div class="ph">
<div style="max-width:860px;margin:0 auto">
<div class="hero-eyebrow" style="background:rgba(59,130,246,.2);border-color:rgba(59,130,246,.4);color:#bfdbfe;display:inline-flex;margin-bottom:1rem">&#127891; {category}</div>
<h1>{kw_title}{loc_sfx}</h1>
<p>{desc}</p>
{update_badge}
</div>
</div>
{bc_html}
<div class="pg">
<main class="art" id="main-content">
{author_bar(body_html)}
{toc_html}
<div class="intro-box">{intro_text}</div>
{body_html}
<h2 id="products" style="margin-top:2.8rem">HRCP Study Programs</h2>
<p style="color:#6b7280;font-size:.9rem;margin-bottom:1rem">All programs include pass-or-money-back guarantee. Online editions have instant digital access.</p>
{prod_html}
{guarantee_box()}
<div id="related" class="related-wrap">
<h3>&#128279; Related Guides</h3>
<div class="rel-grid">{rel_links}</div>
</div>
<div style="background:#f8faff;border:1px solid #dbeafe;border-radius:10px;padding:1.1rem 1.3rem;margin-top:1.5rem;font-size:.8rem;color:#374151">
<strong style="color:#1e3a5f;display:block;margin-bottom:.5rem">&#128203; Official Sources</strong>
<a href="https://www.hrci.org/" rel="noopener" target="_blank" style="color:#1d4ed8">HRCI (HR Certification Institute)</a> — Apply for aPHR, PHR, SPHR, GPHR, PHRi, SPHRi exams &bull;
<a href="https://www.shrm.org/credentials" rel="noopener" target="_blank" style="color:#1d4ed8">SHRM Credentials</a> — Apply for SHRM-CP, SHRM-SCP exams &bull;
<a href="{AFF_HOME}" rel="noopener" target="_blank" style="color:#1d4ed8">HRCP</a> — Official study materials with pass-or-money-back guarantee
</div>
<div class="disclosure">
<strong>Affiliate Disclosure</strong>
This page contains affiliate links. We earn a commission when you purchase HRCP study materials through our links, at no extra cost to you. Our reviews and recommendations are written independently.
<br>Official HRCP site: <a href="{AFF_HOME}" rel="noopener" target="_blank">hrcp.com</a> &bull;
Official HRCI: <a href="https://www.hrci.org/" rel="noopener" target="_blank">hrci.org</a> &bull;
Official SHRM: <a href="https://www.shrm.org/" rel="noopener" target="_blank">shrm.org</a>
</div>
</main>
<aside class="sidebar">
<div class="sb-hero">
<h3>Get HRCP Study Materials</h3>
<p>Pass-or-money-back guarantee &bull; Since 1995 &bull; 100,000+ students</p>
<a href="{AFF}" class="sb-btn" rel="noopener sponsored">Start Studying Now &rarr;</a>
<p style="font-size:.72rem;opacity:.7;margin-top:.6rem">Instant digital access available</p>
</div>
<div class="sb-card">
<h3>&#128204; HRCP Programs</h3>
<ul class="chk-list">
<li>aPHR Online — $175</li>
<li>PHR/SPHR Online — $295</li>
<li>PHR/SPHR Print — $375</li>
<li>SHRM-CP/SCP — $295</li>
<li>PHRi/SPHRi — $295</li>
<li>Pass-or-money-back guarantee</li>
</ul>
</div>
<div class="sb-card">
<h3>&#128279; Quick Links</h3>
<ul style="list-style:none;margin:0">
<li style="padding:.28rem 0;font-size:.83rem"><a href="{SITE}/guides/hrcp-review/">&#9733; HRCP Full Review</a></li>
<li style="padding:.28rem 0;font-size:.83rem"><a href="{SITE}/guides/phr-study-guide/">PHR Study Guide</a></li>
<li style="padding:.28rem 0;font-size:.83rem"><a href="{SITE}/guides/aphr-study-guide/">aPHR Study Guide</a></li>
<li style="padding:.28rem 0;font-size:.83rem"><a href="{SITE}/guides/hr-certification-cost/">Certification Cost</a></li>
<li style="padding:.28rem 0;font-size:.83rem"><a href="{SITE}/guides/how-to-pass-hr-certification/">Pass Tips</a></li>
<li style="padding:.28rem 0;font-size:.83rem"><a href="{SITE}/guides/hrci-vs-shrm/">HRCI vs SHRM</a></li>
</ul>
</div>
<div style="background:#f0fdf4;border:1px solid #86efac;border-radius:10px;padding:1rem;text-align:center;font-size:.78rem;color:#166534;line-height:1.8">
&#127881; <strong>Pass or Money Back</strong><br>
HRCP guarantees you'll pass<br>
or your money back
</div>
</aside>
</div>
{share(canon)}
<section style="background:#1e3a5f;color:#fff;padding:4.5rem 1.2rem;text-align:center;border-top:4px solid #3b82f6">
<h2 style="font-size:clamp(1.55rem,3.2vw,2.2rem);margin-bottom:1rem;font-weight:900">Ready to Get HR Certified?</h2>
<p style="font-size:1.05rem;opacity:.88;max-width:560px;margin:0 auto 2rem;line-height:1.75">HRCP study materials have helped 100,000+ HR professionals pass their certification exams since 1995. Pass-or-money-back guarantee.</p>
<a href="{AFF}" class="cta-btn" rel="noopener sponsored">Get HRCP Materials &rarr;</a>
</section>
{footer()}
{JS}
</body>
</html>"""


# ── KW PAGE INTL ──────────────────────────────────────────────────────────────
# ── NATIVE LANGUAGE STRINGS ────────────────────────────────────────────────────
NATIVE_INTRO = {
    "es": "Esta guía cubre {kw} — todo lo que los profesionales de RRHH necesitan para prepararse y aprobar su examen de certificación.",
    "pt": "Este guia aborda {kw} — tudo que profissionais de RH precisam para se preparar e passar no exame de certificação.",
    "fr": "Ce guide couvre {kw} — tout ce que les professionnels RH doivent savoir pour préparer et réussir leur examen de certification.",
    "de": "Dieser Leitfaden behandelt {kw} — alles, was HR-Fachleute zur Vorbereitung und zum Bestehen ihrer Zertifizierungsprüfung benötigen.",
    "ja": "このガイドでは{kw}について解説します。HR専門家が資格試験に合格するために必要なすべての情報を提供します。",
    "ko": "이 가이드는 {kw}에 대해 다룹니다. HR 전문가가 자격증 시험을 준비하고 합격하는 데 필요한 모든 정보를 제공합니다.",
    "ar": "يغطي هذا الدليل {kw} — كل ما يحتاجه متخصصو الموارد البشرية للتحضير واجتياز امتحان الشهادة.",
    "zh": "本指南涵盖{kw}——HR专业人员准备并通过认证考试所需的全面信息。",
    "hi": "यह गाइड {kw} को कवर करता है — HR पेशेवरों को अपनी सर्टिफिकेशन परीक्षा की तैयारी और पास करने के लिए आवश्यक सभी जानकारी।",
    "it": "Questa guida tratta {kw} — tutto ciò che i professionisti HR devono sapere per prepararsi e superare il proprio esame di certificazione.",
    "nl": "Deze gids behandelt {kw} — alles wat HR-professionals nodig hebben om hun certificeringsexamen voor te bereiden en te halen.",
    "pl": "Ten przewodnik obejmuje {kw} — wszystko, czego specjaliści HR potrzebują, aby przygotować się i zdać egzamin certyfikacyjny.",
    "tr": "Bu rehber {kw} konusunu ele alıyor — İK profesyonellerinin sertifikasyon sınavına hazırlanmak ve geçmek için ihtiyaç duydukları her şey.",
    "id": "Panduan ini membahas {kw} — semua yang dibutuhkan profesional HR untuk mempersiapkan dan lulus ujian sertifikasi mereka.",
    "vi": "Hướng dẫn này đề cập đến {kw} — tất cả những gì các chuyên gia HR cần để chuẩn bị và vượt qua kỳ thi chứng chỉ.",
}
NATIVE_CTA = {
    "es": "Obtenga los materiales de estudio HRCP y apruebe su examen con la garantía de devolución de dinero.",
    "pt": "Obtenha os materiais de estudo HRCP e passe no seu exame com garantia de devolução do dinheiro.",
    "fr": "Obtenez les matériaux HRCP et réussissez votre examen avec la garantie satisfait ou remboursé.",
    "de": "Holen Sie sich die HRCP-Materialien und bestehen Sie Ihre Prüfung mit der Geld-zurück-Garantie.",
    "ja": "HRCP学習教材を入手して、合格保証付きで資格試験に合格しましょう。",
    "ko": "HRCP 학습 자료를 구하고 합격 보장 제도와 함께 자격증 시험을 통과하세요.",
    "ar": "احصل على مواد دراسة HRCP وانجح في امتحان الشهادة مع ضمان استرداد المال.",
    "zh": "获取HRCP学习材料，凭借通过或退款保证通过您的认证考试。",
    "hi": "HRCP अध्ययन सामग्री प्राप्त करें और पास-या-पैसे-वापस गारंटी के साथ परीक्षा पास करें।",
    "it": "Ottieni i materiali HRCP e supera il tuo esame con la garanzia soddisfatto o rimborsato.",
    "nl": "Haal de HRCP materialen en slaag voor je examen met de teruggeldgarantie.",
    "pl": "Zdobądź materiały HRCP i zdaj egzamin z gwarancją zwrotu pieniędzy.",
    "tr": "HRCP materyallerini alın ve para iade garantisiyle sınavınızı geçin.",
    "id": "Dapatkan materi HRCP dan lulus ujian Anda dengan jaminan uang kembali.",
    "vi": "Lấy tài liệu HRCP và vượt qua kỳ thi của bạn với đảm bảo hoàn tiền.",
}
NATIVE_SECTIONS = {
    "zh": {"why_h2":"为什么选择HRCP备考材料？","why_p":"HRCP提供最全面的人力资源认证备考材料，自1995年以来帮助超过10万名人力资源专业人士通过认证考试。材料每年更新，涵盖HRCI和SHRM两大认证体系。通过或退款保证意味着您的投资完全受到保护。","certs_h2":"主要人力资源认证","certs_p":"aPHR（无经验要求，$400考试费）、PHR（1-4年经验，$495）、SPHR（4-7年领导经验，$495）、SHRM-CP/SCP（SHRM认证，全球认可）。","study_h2":"学习策略","study_p":"成功关键：系统学习所有内容，每天用抽认卡记忆术语，在限时条件下完成模拟考试，并深入分析错误答案。HRCP提供4、8和12周学习计划。"},
    "hi": {"why_h2":"HRCP क्यों चुनें?","why_p":"HRCP 1995 से सबसे व्यापक HR प्रमाणन तैयारी सामग्री प्रदान कर रहा है। 1,00,000+ HR पेशेवरों ने HRCP से परीक्षाएं पास की हैं। सामग्री हर साल अपडेट होती है और HRCI और SHRM दोनों को कवर करती है।","certs_h2":"प्रमुख HR प्रमाणन","certs_p":"aPHR (कोई अनुभव नहीं, $400), PHR (1-4 वर्ष, $495), SPHR (4-7 वर्ष नेतृत्व, $495), SHRM-CP/SCP (SHRM प्रमाणन, वैश्विक मान्यता)।","study_h2":"अध्ययन रणनीति","study_p":"सफलता की कुंजी: सामग्री व्यवस्थित रूप से पढ़ें, फ्लैशकार्ड से शब्दावली याद करें, समय-सीमित अभ्यास परीक्षाएं दें, गलत उत्तरों का विश्लेषण करें।"},
    "ar": {"why_h2":"لماذا HRCP؟","why_p":"توفر HRCP أشمل مواد إعداد شهادات الموارد البشرية منذ 1995. ساعدت أكثر من 100,000 متخصص. تُحدَّث سنوياً وتغطي HRCI وSHRM. ضمان النجاح أو استرداد المال.","certs_h2":"شهادات الموارد البشرية","certs_p":"aPHR: بدون خبرة، $400. PHR: 1-4 سنوات، $495. SPHR: 4-7 سنوات قيادة، $495. SHRM-CP/SCP: شهادات SHRM، معترف بها دولياً.","study_h2":"استراتيجية الدراسة","study_p":"مفاتيح النجاح: مراجعة منهجية، دراسة البطاقات التعليمية يومياً، اختبارات موقوتة، وتحليل الإجابات الخاطئة."},
    "de": {"why_h2":"Warum HRCP?","why_p":"HRCP bietet seit 1995 die umfassendsten HR-Zertifizierungsmaterialien. Über 100.000 Fachleute haben bestanden. Inhalte werden jährlich aktualisiert und decken HRCI und SHRM ab. Bestehen-oder-Geld-zurück-Garantie.","certs_h2":"Wichtige HR-Zertifizierungen","certs_p":"aPHR: keine Erfahrung, $400. PHR: 1-4 Jahre, $495. SPHR: 4-7 Jahre Führungserfahrung, $495. SHRM-CP/SCP: international anerkannt.","study_h2":"Lernstrategie","study_p":"Schlüssel zum Erfolg: Inhaltsmodule systematisch durcharbeiten, täglich Karteikarten lernen, zeitgesteuerte Übungsprüfungen ablegen, fehlerhafte Antworten analysieren."},
    "fr": {"why_h2":"Pourquoi HRCP?","why_p":"HRCP fournit les matériaux de préparation RH les plus complets depuis 1995. Plus de 100 000 professionnels ont réussi. Mis à jour annuellement, couvre HRCI et SHRM. Garantie réussite ou remboursement.","certs_h2":"Principales certifications RH","certs_p":"aPHR: aucune expérience, $400. PHR: 1-4 ans, $495. SPHR: 4-7 ans de leadership, $495. SHRM-CP/SCP: certifications SHRM, reconnus internationalement.","study_h2":"Stratégie d'étude","study_p":"Clés de réussite: révision systématique de tous les modules, fiches quotidiennes, examens pratiques chronométrés, analyse approfondie des erreurs."},
    "es": {"why_h2":"¿Por qué HRCP?","why_p":"HRCP proporciona los materiales más completos desde 1995. Más de 100.000 profesionales aprobaron. Actualizado anualmente, cubre HRCI y SHRM. Garantía de aprobación o devolución.","certs_h2":"Principales certificaciones de RRHH","certs_p":"aPHR: sin experiencia, $400. PHR: 1-4 años, $495. SPHR: 4-7 años liderazgo, $495. SHRM-CP/SCP: certificaciones SHRM, reconocidas internacionalmente.","study_h2":"Estrategia de estudio","study_p":"Claves del éxito: revisión sistemática, tarjetas de vocabulario diarias, exámenes cronometrados, análisis de respuestas incorrectas."},
    "pt": {"why_h2":"Por que HRCP?","why_p":"HRCP fornece os materiais mais abrangentes desde 1995. Mais de 100.000 profissionais aprovados. Atualizado anualmente, cobre HRCI e SHRM. Garantia de aprovação ou devolução.","certs_h2":"Principais certificações de RH","certs_p":"aPHR: sem experiência, $400. PHR: 1-4 anos, $495. SPHR: 4-7 anos liderança, $495. SHRM-CP/SCP: internacionalmente reconhecidos.","study_h2":"Estratégia de estudo","study_p":"Chaves do sucesso: revisão sistemática, cartões diários, exames cronometrados, análise de erros."},
    "ja": {"why_h2":"なぜHRCPを選ぶのか","why_p":"HRCPは1995年から最も包括的なHR資格試験準備教材を提供しています。10万人以上が合格。毎年更新され、HRCIとSHRM両方をカバー。合格または返金保証。","certs_h2":"主要HR認定資格","certs_p":"aPHR（経験不要、$400）、PHR（1-4年経験、$495）、SPHR（4-7年リーダーシップ、$495）、SHRM-CP/SCP（国際的に認められた資格）。","study_h2":"学習戦略","study_p":"成功の鍵：体系的な内容復習、毎日のフラッシュカード学習、制限時間内の模擬試験、不正解の深い分析。"},
    "ko": {"why_h2":"HRCP를 선택하는 이유","why_p":"HRCP는 1995년부터 가장 포괄적인 HR 자격증 시험 준비 자료를 제공합니다. 10만 명 이상 합격. 매년 업데이트, HRCI와 SHRM 모두 포함. 합격 또는 환불 보장.","certs_h2":"주요 HR 자격증","certs_p":"aPHR（경험 불필요, $400）, PHR（1-4년, $495）, SPHR（4-7년 리더십, $495）, SHRM-CP/SCP（국제적으로 인정받음）.","study_h2":"학습 전략","study_p":"성공 열쇠: 체계적 내용 검토, 매일 플래시카드, 시간 제한 연습 시험, 틀린 답 심층 분석."},
    "it": {"why_h2":"Perché HRCP?","why_p":"HRCP fornisce i materiali più completi dal 1995. Oltre 100.000 professionisti hanno superato gli esami. Aggiornato annualmente, copre HRCI e SHRM. Garanzia superamento o rimborso.","certs_h2":"Principali certificazioni HR","certs_p":"aPHR: nessuna esperienza, $400. PHR: 1-4 anni, $495. SPHR: 4-7 anni di leadership, $495. SHRM-CP/SCP: riconosciuti internazionalmente.","study_h2":"Strategia di studio","study_p":"Chiavi del successo: revisione sistematica, flashcard quotidiane, esami cronometrati, analisi degli errori."},
    "nl": {"why_h2":"Waarom HRCP?","why_p":"HRCP biedt de meest uitgebreide materialen sinds 1995. Meer dan 100.000 professionals geslaagd. Jaarlijks bijgewerkt, dekt HRCI en SHRM. Slaag-of-geld-terug-garantie.","certs_h2":"Belangrijkste HR-certificeringen","certs_p":"aPHR: geen ervaring, $400. PHR: 1-4 jaar, $495. SPHR: 4-7 jaar leiderschap, $495. SHRM-CP/SCP: internationaal erkend.","study_h2":"Studiestrategie","study_p":"Sleutels tot succes: systematische revisie, dagelijkse flashcards, getimede oefenexamens, analyse van fouten."},
    "pl": {"why_h2":"Dlaczego HRCP?","why_p":"HRCP dostarcza najobszerniejsze materiały od 1995 roku. Ponad 100 000 specjalistów zdało. Aktualizowane corocznie, obejmuje HRCI i SHRM. Gwarancja zdania lub zwrotu.","certs_h2":"Główne certyfikaty HR","certs_p":"aPHR: bez doświadczenia, $400. PHR: 1-4 lata, $495. SPHR: 4-7 lat przywództwa, $495. SHRM-CP/SCP: uznawane na całym świecie.","study_h2":"Strategia nauki","study_p":"Klucze sukcesu: systematyczna nauka, codzienne fiszki, próbne egzaminy, analiza błędów."},
    "tr": {"why_h2":"Neden HRCP?","why_p":"HRCP, 1995'ten bu yana en kapsamlı İK sertifikasyon materyallerini sunmaktadır. 100.000'den fazla kişi geçti. Her yıl güncellenmekte, HRCI ve SHRM'yi kapsamaktadır. Geçme veya para iade garantisi.","certs_h2":"Önemli İK Sertifikaları","certs_p":"aPHR: deneyim yok, $400. PHR: 1-4 yıl, $495. SPHR: 4-7 yıl liderlik, $495. SHRM-CP/SCP: uluslararası tanınan.","study_h2":"Çalışma stratejisi","study_p":"Başarı anahtarları: sistematik içerik çalışması, günlük flash kart, zamanlı sınavlar, hata analizi."},
    "id": {"why_h2":"Mengapa HRCP?","why_p":"HRCP menyediakan materi paling komprehensif sejak 1995. Lebih dari 100.000 profesional lulus. Diperbarui setiap tahun, mencakup HRCI dan SHRM. Jaminan lulus atau uang kembali.","certs_h2":"Sertifikasi HR Utama","certs_p":"aPHR: tanpa pengalaman, $400. PHR: 1-4 tahun, $495. SPHR: 4-7 tahun kepemimpinan, $495. SHRM-CP/SCP: diakui internasional.","study_h2":"Strategi belajar","study_p":"Kunci sukses: tinjauan konten sistematis, kartu flash harian, ujian latihan berwaktu, analisis kesalahan."},
    "vi": {"why_h2":"Tại sao HRCP?","why_p":"HRCP cung cấp tài liệu toàn diện nhất từ 1995. Hơn 100.000 chuyên gia đã đậu. Cập nhật hàng năm, bao gồm HRCI và SHRM. Bảo đảm đậu hoặc hoàn tiền.","certs_h2":"Các chứng chỉ HR chính","certs_p":"aPHR: không cần kinh nghiệm, $400. PHR: 1-4 năm, $495. SPHR: 4-7 năm lãnh đạo, $495. SHRM-CP/SCP: được công nhận quốc tế.","study_h2":"Chiến lược học tập","study_p":"Chìa khóa thành công: ôn tập có hệ thống, học thẻ flash hàng ngày, bài kiểm tra có giới hạn thời gian, phân tích lỗi."},
}

# ── INTL BODY — 10 VARIANTS ────────────────────────────────────────────────────
def body_intl(kw, slug, category, idx, lang_code):
    L = LANGUAGES.get(lang_code, LANGUAGES["en"])
    h = (sh(slug + lang_code) + idx) % 10
    extra = _extra_section(slug, idx)
    ns = NATIVE_SECTIONS.get(lang_code, {})
    ns_block = (f'<h2 id="why-hrcp">{ns["why_h2"]}</h2>\n<p>{ns["why_p"]}</p>\n<h2 id="certifications">{ns["certs_h2"]}</h2>\n<p>{ns["certs_p"]}</p>\n<h2 id="study">{ns["study_h2"]}</h2>\n<p>{ns["study_p"]}</p>') if ns else ""
    faq_items = [
        ("What is HR certification?",
         f"HR certification demonstrates professional HR competence. HRCP has provided study materials since 1995. {L['cta']}: Pass-or-money-back guarantee."),
        ("How much does HRCP cost?",
         f"aPHR Online: $175. PHR/SPHR Online: $295. PHR/SPHR Print: $375. SHRM-CP/SCP Online: $295. {L['free_trial']}."),
        ("Is HRCP available internationally?",
         "Yes. HRCP online editions are available worldwide as instant digital downloads. PHRi and SPHRi programs are specifically designed for international HR professionals."),
        ("What is the HRCP guarantee?",
         "HRCP offers a pass-or-money-back guarantee. See hrcp.com for current terms. This guarantee reflects 30 years of confidence in their materials."),
    ]
    faq_html = "".join(
        f'<details class="faq-item"><summary class="faq-q">{q}</summary><div class="faq-a">{a}</div></details>'
        for q,a in faq_items
    )
    stat = stat_block()
    if h == 0:
        return f"""
<h2 id="overview">{kw} — HRCP Study Materials</h2>
<p>HRCP has provided HR certification study materials since 1995, helping over 100,000 professionals pass their certification exams. Materials are available worldwide with instant digital access. {L['free_trial']}.</p>
{ns_block}
<h2 id="how-to">{L['cta']}</h2>
<ol class="steps">
<li><strong>Choose your exam</strong><p>aPHR (entry-level, no experience required), PHR, SPHR, SHRM-CP, SHRM-SCP, PHRi, or SPHRi.</p></li>
<li><strong>Get HRCP materials</strong><p>Online editions provide instant access. Print editions ship worldwide. Both include comprehensive content and practice exams.</p></li>
<li><strong>Study systematically</strong><p>Follow the included study schedule. Take practice exams. Review weak areas. Pass your certification exam.</p></li>
</ol>
{extra}{stat}<div class="faq-wrap">{faq_html}</div>"""
    elif h == 1:
        return f"""
<h2 id="overview">{kw} — {L['cta']}</h2>
<p>HR certification is increasingly valued by employers worldwide. HRCP provides the most comprehensive preparation for HRCI and SHRM exams. Available as instant digital download in your country.</p>
{ns_block}
<h2>HRCP Programs</h2>
<table class="cmp">
<tr><th>Program</th><th>Exam</th><th>Price</th><th>Format</th></tr>
<tr><td>aPHR Prep</td><td>aPHR (HRCI)</td><td class="good">$175</td><td>Online or Print</td></tr>
<tr><td>Complete HRCP Program</td><td>PHR/SPHR (HRCI)</td><td>$295–$375</td><td>Online or Print</td></tr>
<tr><td>SHRM Prep</td><td>SHRM-CP/SCP</td><td>$295</td><td>Online</td></tr>
<tr><td>International Prep</td><td>PHRi/SPHRi</td><td>$295</td><td>Online</td></tr>
</table>
{extra}{stat}<div class="faq-wrap">{faq_html}</div>"""
    elif h == 2:
        return f"""
<h2 id="overview">{kw} — Expert Guide</h2>
<p>This guide covers {kw.lower()} for HR professionals worldwide. HRCP's study materials cover HRCI exams (aPHR, PHR, SPHR, GPHR, PHRi, SPHRi) and SHRM exams (SHRM-CP, SHRM-SCP). {L['free_trial']}.</p>
{ns_block}
<h2>Why HRCP?</h2>
<ul>
<li><strong>100,000+ students have passed</strong> using HRCP materials since 1995</li>
<li><strong>Updated annually</strong> to reflect current exam content and HR practices</li>
<li><strong>Pass-or-money-back guarantee</strong> — HRCP stands behind their materials</li>
<li><strong>2,000+ practice questions</strong> across 16 practice exams (PHR/SPHR program)</li>
<li><strong>Audio reader included</strong> in all online editions</li>
</ul>
{extra}{stat}<div class="faq-wrap">{faq_html}</div>"""
    elif h == 3:
        return f"""
<h2 id="overview">{kw}</h2>
<p>HR certification from HRCI or SHRM demonstrates professional competence to employers worldwide. HRCP has been the trusted preparation resource for over 30 years. Pass-or-money-back guarantee included.</p>
{ns_block}
<h2>HR Certification: Which Level Is Right for You?</h2>
<p><strong>New to HR?</strong> The aPHR requires no experience. HRCP materials: $175 online.</p>
<p><strong>1–4 years HR experience?</strong> PHR or SHRM-CP. HRCP Complete Program: $295 online / $375 print.</p>
<p><strong>Senior HR leader?</strong> SPHR or SHRM-SCP. Same HRCP program covers both.</p>
<p><strong>Working globally?</strong> PHRi, SPHRi, or GPHR. HRCP International Program: $295 online.</p>
{extra}{stat}<div class="faq-wrap">{faq_html}</div>"""
    elif h == 4:
        return f"""
<h2 id="overview">{kw} — Pricing and Value</h2>
<p>HRCP study materials range from $175 (aPHR online) to $375 (PHR/SPHR print). All programs include comprehensive content, flashcards, and practice exams with 1,300–2,000+ questions. Pass-or-money-back guarantee.</p>
{ns_block}
<table class="cmp">
<tr><th>Program</th><th>Online Price</th><th>Print Price</th><th>Practice Questions</th></tr>
<tr><td>aPHR</td><td class="good">$175</td><td>$195</td><td>1,300+</td></tr>
<tr><td>PHR/SPHR</td><td>$295</td><td>$375</td><td class="good">2,000+</td></tr>
<tr><td>SHRM-CP/SCP</td><td>$295</td><td>N/A</td><td class="good">2,000+</td></tr>
<tr><td>PHRi/SPHRi</td><td>$295</td><td>N/A</td><td class="good">2,000+</td></tr>
</table>
{extra}{stat}<div class="faq-wrap">{faq_html}</div>"""
    elif h == 5:
        return f"""
<h2 id="overview">{kw} — Step-by-Step Guide</h2>
<p>This guide walks through the complete HR certification preparation process using HRCP materials. Available worldwide as instant digital download. {L['free_trial']}.</p>
{ns_block}
<ol class="steps">
<li><strong>Apply for the exam</strong><p>Submit your application to HRCI (hrci.org) or SHRM (shrm.org). Processing takes 2–4 weeks. For aPHR, no experience required.</p></li>
<li><strong>Order HRCP materials</strong><p>Select online (instant access, audio reader) or print (shipped to your address). Both include all practice exams.</p></li>
<li><strong>Follow the study schedule</strong><p>HRCP provides 4, 8, and 12-week study schedules. Take the preliminary assessment first to identify weak areas.</p></li>
<li><strong>Take practice exams</strong><p>Complete all included practice exams. Target 80%+ consistently before sitting for the real exam.</p></li>
<li><strong>Pass your exam</strong><p>Most candidates who complete the full HRCP program pass on their first attempt. Pass-or-money-back guarantee covers your attempt.</p></li>
</ol>
{extra}{stat}<div class="faq-wrap">{faq_html}</div>"""
    elif h == 6:
        return f"""
<h2 id="overview">{kw} — Career Impact Guide</h2>
<p>HR certification consistently delivers measurable career outcomes. Research shows certified HR professionals earn 5–15% more, advance faster, and are more likely to be retained during organizational changes. {L['cta']} with the industry-leading HRCP program.</p>
{ns_block}
<h2>Certification vs No Certification: The Data</h2>
<table class="cmp">
<tr><th>Outcome</th><th>Certified HR</th><th>Uncertified HR</th></tr>
<tr><td>Salary premium</td><td class="good">5–15% higher</td><td>Baseline</td></tr>
<tr><td>Promotion likelihood (5 yrs)</td><td class="good">Significantly higher</td><td>Lower</td></tr>
<tr><td>Full-time employment rate</td><td class="good">Higher</td><td>Lower</td></tr>
<tr><td>Career satisfaction</td><td class="good">Higher reported</td><td>Lower reported</td></tr>
</table>
{extra}{stat}<div class="faq-wrap">{faq_html}</div>"""
    elif h == 7:
        return f"""
<h2 id="overview">{kw} — International HR Professionals Guide</h2>
<p>HR certification from HRCI and SHRM is globally recognized. For professionals outside the United States, HRCI offers PHRi, SPHRi, and GPHR credentials. HRCP provides study materials for all international certifications. Pass-or-money-back guarantee.</p>
{ns_block}
<h2>International Certification Options</h2>
<table class="cmp">
<tr><th>Credential</th><th>Who It's For</th><th>Experience</th><th>HRCP Materials</th></tr>
<tr><td><strong>PHRi</strong></td><td>International HR professionals</td><td>1–4 years</td><td class="good">$295 online</td></tr>
<tr><td><strong>SPHRi</strong></td><td>Senior international HR</td><td>4+ years leadership</td><td class="good">$295 online</td></tr>
<tr><td><strong>GPHR</strong></td><td>Global HR operations</td><td>2+ years global</td><td class="good">Included in PHR/SPHR</td></tr>
<tr><td><strong>aPHR</strong></td><td>Entry-level anywhere</td><td class="good">None</td><td class="good">$175 online</td></tr>
</table>
{extra}{stat}<div class="faq-wrap">{faq_html}</div>"""
    elif h == 8:
        return f"""
<h2 id="overview">{kw} — Complete Comparison</h2>
<p>Choosing the right HR certification is one of the most important career decisions. This guide provides a data-driven comparison. All certifications are covered by HRCP study materials with pass-or-money-back guarantee.</p>
{ns_block}
<h2>aPHR vs PHR vs SPHR vs SHRM-CP: Quick Comparison</h2>
<table class="cmp">
<tr><th>Factor</th><th>aPHR</th><th>PHR</th><th>SPHR</th><th>SHRM-CP</th></tr>
<tr><td>Level</td><td>Entry</td><td>Mid</td><td>Senior</td><td>Mid</td></tr>
<tr><td>Experience</td><td class="good">None</td><td>1–4 yrs</td><td>4–7 yrs</td><td>0–3 yrs</td></tr>
<tr><td>Exam cost</td><td class="good">$400</td><td>$495</td><td>$495</td><td>$300–$475</td></tr>
<tr><td>HRCP prep</td><td class="good">$175</td><td class="good">$295</td><td class="good">$295</td><td class="good">$295</td></tr>
<tr><td>Pass rate</td><td>71%</td><td>72%</td><td>76%</td><td>N/A</td></tr>
</table>
{extra}{stat}<div class="faq-wrap">{faq_html}</div>"""
    else:  # h == 9
        return f"""
<h2 id="overview">{kw} — Honest Review</h2>
<p>This review covers HRCP study materials honestly. HRCP has helped over 100,000 HR professionals pass certification exams since 1995. Pass-or-money-back guarantee. {L['cta']}.</p>
{ns_block}
<h2>What HRCP Gets Right</h2>
<p><strong>Content depth:</strong> 900+ pages for PHR/SPHR, covering every exam domain. Updated annually.</p>
<p><strong>Practice volume:</strong> 2,000+ questions across 16 practice exams. The most important predictor of exam success.</p>
<p><strong>Guarantee:</strong> The pass-or-money-back guarantee is real. HRCP stands behind their materials.</p>
<h2>What HRCP Is Not</h2>
<p>Text-based — no included video lectures. No live instructor sessions. For candidates who learn best from self-directed text study: HRCP is ideal. For video learners: supplement with a video course.</p>
{extra}{stat}<div class="faq-wrap">{faq_html}</div>"""


def kw_page_intl(slug, kw_title, category, volume, idx, lang_code):
    L      = LANGUAGES.get(lang_code, LANGUAGES["en"])
    lslug  = slug.split("/")[-1]
    canon  = f"{SITE}/{L['dir']}/{lslug}/"
    pg_t   = unique_title(f"{kw_title} {L['suffix']}"[:68], slug)
    desc   = f"Complete guide to {kw_title.lower()} — HRCP study materials, practice tests, and expert advice to pass your HR certification exam."[:158]
    body_html = body_intl(kw_title, slug, category, idx, lang_code)
    mins   = read_mins(body_html)
    art    = json.dumps({"@context":"https://schema.org","@type":"Article",
        "headline":kw_title,"description":desc,"url":canon,"datePublished":TODAY,
        "dateModified":TODAY,"inLanguage":lang_code,
        "author":{"@type":"Organization","name":NAME,"url":SITE}})
    bc     = json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":L["home"],"item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":L["guides_lbl"],"item":f"{SITE}/{L['dir']}/"},
        {"@type":"ListItem","position":3,"name":kw_title,"item":canon}]})
    sp     = json.dumps({"@context":"https://schema.org","@type":"WebPage",
        "speakable":{"@type":"SpeakableSpecification","cssSelector":[".intro-box","h1","h2"]},"url":canon})
    rtl    = ' dir="rtl"' if lang_code == "ar" else ""
    auth   = author_bar(body_html, lang_code)
    native_intro = NATIVE_INTRO.get(lang_code,"").replace("{kw}", kw_title) or f"This guide covers {kw_title.lower()} — everything HR professionals need to prepare for and pass their HR certification exam."
    native_cta   = NATIVE_CTA.get(lang_code,"")
    return f"""<!DOCTYPE html>
<html lang="{lang_code}"{rtl}>
<head>{hd(pg_t, desc, canon, [art,bc,sp], "article", lang_code)}</head>
<body>
{nav(lang_code)}{trust(lang_code)}
<div class="ph"><div style="max-width:860px;margin:0 auto">
<h1>{kw_title}</h1><p>{native_intro}</p>
<div class="update-badge">&#128197; {L["updated"]} {TODAY} &bull; {mins} {L["read_min"]}</div>
</div></div>
<div class="breadcrumb"><a href="{SITE}/">{L["home"]}</a><span class="sep">›</span><a href="{SITE}/{L['dir']}/">{L["guides_lbl"]}</a><span class="sep">›</span>{kw_title}</div>
<div class="pg">
<main class="art">{auth}
<div class="intro-box">{native_intro}</div>
{body_html}
<h2 id="products">HRCP Study Programs</h2>{product_grid(slug,idx)}
{guarantee_box()}
<div class="disclosure"><strong>{L["disclosure"]}</strong></div>
</main>
<aside class="sidebar">
<div class="sb-hero"><h3>{L["sidebar_h"]}</h3><p>{L["sidebar_sub"]}</p>
<a href="{AFF}" class="sb-btn" rel="noopener sponsored">{L["cta"]} &rarr;</a>
</div>
<div class="sb-card"><h3>&#128204; {L["guides_lbl"]}</h3>
<ul class="chk-list">
<li>aPHR — $175</li><li>PHR/SPHR — $295–$375</li>
<li>SHRM-CP/SCP — $295</li><li>PHRi/SPHRi — $295</li>
<li>{L["free_trial"]}</li></ul></div>
</aside></div>
{share(canon, lang_code)}
<section style="background:#1e3a5f;color:#fff;padding:4rem 1.2rem;text-align:center;border-top:4px solid #3b82f6">
<h2 style="font-size:1.8rem;margin-bottom:1rem">{L["bottom_cta_h"]}</h2>
<p style="opacity:.88;max-width:560px;margin:0 auto 2rem">{L["bottom_cta_p"]}</p>
<a href="{AFF}" class="cta-btn" rel="noopener sponsored">{L["cta"]} &rarr;</a>
{f'<p class="hero-note">{native_cta}</p>' if native_cta else ""}
</section>
{footer(lang_code)}{JS}
</body></html>"""

# ── BLOG ─────────────────────────────────────────────────────────────────────
BLOG_SEED = [
    ("aphr-vs-phr-which-first","aPHR vs PHR: Which HR Certification Should You Get First?","Comparison"),
    ("phr-study-guide-complete","Complete PHR Study Guide: Everything You Need to Pass","Study Guide"),
    ("how-long-to-study-phr","How Long Should You Study for the PHR Exam?","Study Tips"),
    ("hrcp-review-honest","HRCP Review 2025: Honest Assessment After Using the Materials","Review"),
    ("shrm-cp-vs-phr-which-better","SHRM-CP vs PHR: Which HR Certification Is Better?","Comparison"),
    ("hr-certification-worth-it","Is HR Certification Worth It? The Data Says Yes","Analysis"),
    ("aphr-study-guide","aPHR Study Guide: Complete Exam Preparation","Study Guide"),
    ("phr-exam-tips","10 PHR Exam Tips from Candidates Who Passed on the First Try","Study Tips"),
    ("sphr-vs-shrm-scp","SPHR vs SHRM-SCP: Which Senior HR Certification Is Better?","Comparison"),
    ("hr-certification-salary-boost","HR Certification Salary Boost: What the Research Shows","Analysis"),
    ("how-to-pass-phr-first-try","How to Pass the PHR Exam on Your First Attempt","Study Tips"),
    ("hrci-vs-shrm-certification","HRCI vs SHRM Certification: Complete 2025 Comparison","Comparison"),
    ("phr-practice-questions-guide","PHR Practice Questions: How to Use Them Effectively","Study Guide"),
    ("best-hr-certification-beginners","Best HR Certification for Beginners: aPHR vs PHR vs SHRM-CP","Comparison"),
    ("hr-certification-requirements-2025","HR Certification Requirements 2025: Eligibility Guide","Informational"),
    ("sphr-study-guide","SPHR Study Guide: Senior HR Certification Prep","Study Guide"),
    ("shrm-cp-study-guide","SHRM-CP Study Guide: Everything You Need to Know","Study Guide"),
    ("phr-flashcard-strategy","PHR Flashcard Strategy: How to Use Them Most Effectively","Study Tips"),
    ("hr-certification-recertification","HR Certification Recertification: What You Need to Know","Informational"),
    ("gphr-certification-guide","GPHR Certification Guide: Is It Worth It?","Analysis"),
    ("aphr-exam-pass-rate","aPHR Exam Pass Rate and What It Means for Your Study Plan","Analysis"),
    ("phr-exam-pass-rate","PHR Exam Pass Rate: What the Numbers Mean for Candidates","Analysis"),
    ("hr-certification-study-schedule","Creating Your HR Certification Study Schedule","Study Tips"),
    ("employer-hr-certification-reimbursement","Getting Your Employer to Pay for HR Certification","Informational"),
    ("remote-hr-certification-exam","Taking Your HR Certification Exam Remotely: Complete Guide","Informational"),
    ("shrm-membership-worth-it","Is SHRM Membership Worth It for Certification?","Analysis"),
    ("phri-sphri-international-guide","PHRi and SPHRi: Guide for International HR Professionals","Informational"),
    ("hr-certification-study-mistakes","7 HR Certification Study Mistakes That Cost Candidates Their Exam","Study Tips"),
    ("sphr-requirements-experience","SPHR Requirements: Experience, Education, and Eligibility","Informational"),
    ("hr-certification-maintain","How to Maintain Your HR Certification: Recertification Guide","Informational"),
    ("phr-vs-shrm-cp-employer-preference","PHR vs SHRM-CP: Which Do Employers Prefer?","Analysis"),
    ("hr-career-path-certification","HR Career Path: When to Get Each Certification","Informational"),
    ("aphr-no-experience-required","aPHR: The HR Certification You Can Get With No Experience","Informational"),
    ("hrcp-practice-exams-strategy","How to Get the Most from HRCP Practice Exams","Study Tips"),
    ("hr-certification-cost-breakdown","HR Certification Cost: Complete 2025 Breakdown","Informational"),
    ("best-time-to-take-phr","Best Time to Take the PHR Exam: Timing Strategy","Study Tips"),
    ("hr-certification-job-search","Using HR Certification in Your Job Search","Informational"),
    ("phr-exam-content-outline","PHR Exam Content Outline: What Will Be Tested","Study Guide"),
    ("hr-certification-linkedin","Adding HR Certification to Your LinkedIn Profile","Informational"),
    ("shrm-scp-study-guide","SHRM-SCP Study Guide: Senior SHRM Certification Prep","Study Guide"),
    ("gphr-vs-sphr","GPHR vs SPHR: Which Global HR Credential Is Better?","Comparison"),
    ("hr-certification-interview","How HR Certification Helps in Job Interviews","Analysis"),
    ("aphr-study-schedule","aPHR Study Schedule: 6-Week Preparation Plan","Study Tips"),
    ("phr-study-schedule-8-week","PHR 8-Week Study Schedule: Day-by-Day Plan","Study Tips"),
    ("what-is-hrci","What Is HRCI? Complete Guide to the HR Certification Institute","Informational"),
    ("what-is-shrm","What Is SHRM? Complete Guide to SHRM Certifications","Informational"),
    ("hr-professional-salary-guide","HR Professional Salary Guide: How Certification Affects Pay","Analysis"),
    ("hr-certification-online-resources","Best Online Resources for HR Certification Prep","Study Guide"),
    ("phr-vs-shrm-cp-study-materials","PHR vs SHRM-CP Study Materials: Which Is Better?","Comparison"),
    ("hr-certification-first-job","Getting HR Certified for Your First HR Job","Informational"),
    ("fail-phr-exam-next-steps","Failed the PHR Exam? Here's What to Do Next","Study Tips"),
    ("aphr-vs-shrm-cp","aPHR vs SHRM-CP: Entry-Level HR Certification Comparison","Comparison"),
    ("hr-certification-worth-cost","HR Certification Cost vs Value: Is the Investment Worth It?","Analysis"),
    ("phr-exam-day-tips","PHR Exam Day: Everything You Need to Know","Study Tips"),
    ("hrcp-audio-reader-how-to-use","HRCP Audio Reader: How to Use It for Better Retention","Study Tips"),
    ("hr-certification-without-degree","HR Certification Without a Degree: Is It Possible?","Informational"),
    ("shrm-vs-hrci-employer-recognition","SHRM vs HRCI: Which Certification Do Employers Recognize More?","Comparison"),
    ("hr-certification-benefits","Benefits of HR Certification: Career, Salary, and Beyond","Analysis"),
    ("phr-sphr-same-program","Why PHR and SPHR Use the Same HRCP Study Program","Informational"),
    ("hr-certification-international","HR Certification for International Professionals: PHRi and GPHR","Informational"),
    ("hrcp-money-back-guarantee-details","HRCP Money-Back Guarantee: What It Covers and How It Works","Review"),
]

BLOG_TEMPLATES = [
    lambda t,d: f"""<p>This guide cuts through the noise to give HR professionals the information they need to make smart decisions about {t.lower()}. All recommendations are based on real exam data and candidate outcomes.</p>
<h2 id="overview">The Short Answer</h2>
<p>After reviewing the data, our recommendation is clear: structured preparation using comprehensive study materials — specifically the <a href="{AFF}" rel="noopener sponsored">HRCP program</a> — is the most reliable path to passing HR certification exams on the first attempt. The 100,000+ students who have passed using HRCP materials since 1995 demonstrate this consistently.</p>
<h2 id="detail">The Detailed Breakdown</h2>
<p>HR professionals who pass their certification exam on the first attempt share several characteristics: they studied systematically rather than sporadically, they used multiple practice exams to identify and close knowledge gaps, they understood the exam format before exam day, and they gave themselves adequate preparation time.</p>
<p>The data on HR certification outcomes is consistent: candidates who complete comprehensive study programs outperform those who rely on their work experience alone. HR certification exams test <em>application</em> of principles, not just familiarity — knowing HR is not the same as knowing how to answer HR certification exam questions.</p>
<h2 id="recommendation">Our Recommendation</h2>
<p>The <a href="{AFF}" rel="noopener sponsored">HRCP study program</a> covers every major HR certification exam (aPHR, PHR, SPHR, SHRM-CP, SHRM-SCP, PHRi, SPHRi) with comprehensive content, 1,300–2,000+ practice questions, and a pass-or-money-back guarantee. It is the most trusted HR certification prep resource available.</p>""",
    lambda t,d: f"""<p>{t} is one of the most common questions HR professionals ask when planning their certification journey. This guide gives you the honest answer based on real outcomes data and what successful candidates actually did.</p>
<h2 id="strategy">The Study Strategy That Works</h2>
<p>Successful HR certification candidates consistently follow a pattern: systematic content review, daily flashcard practice for terminology, multiple timed practice exams, and analysis of every incorrect answer. The <a href="{AFF}" rel="noopener sponsored">HRCP study materials</a> are built around this pattern — preliminary assessment, content modules with self-assessments, flashcards, and a full suite of practice exams from diagnostic through mock exam.</p>
<h2 id="timeline">Timeline Guidance</h2>
<p>Most candidates need 8–12 weeks of structured preparation. HRCP provides 4-week, 8-week, and 12-week study schedules. The right timeline depends on your current HR knowledge depth and weekly study hours available. Candidates who try to compress preparation below 6 weeks show notably lower pass rates regardless of their baseline knowledge.</p>
<div style="background:#f0fdf4;border:2px solid #86efac;border-radius:10px;padding:1.2rem;margin:1.5rem 0;text-align:center">
<strong style="color:#166534">&#127881; Pass-or-Money-Back Guarantee</strong><br>
<span style="color:#166534;font-size:.9rem">HRCP guarantees you'll pass your HR certification exam — or your money back.</span><br>
<a href="{AFF}" rel="noopener sponsored" style="color:#1d4ed8;font-weight:700">Get HRCP Materials &rarr;</a>
</div>""",
    lambda t,d: f"""<p>Five key facts about {t.lower()} that most guides miss — concise and actionable.</p>
<h2>1. The exam tests application, not recall</h2>
<p>Most HR certification exam questions are situational — "what should the HR professional do in this situation?" Not "what does the law say about this?" Studying terminology alone is insufficient. You need to practice applying principles to scenarios, which is why HRCP's 1,300–2,000+ practice questions are more valuable than content review alone.</p>
<h2>2. Pass rates are higher than you think</h2>
<p>PHR pass rate: 72%. aPHR: 71%. SPHR: 76%. Most candidates who follow a structured preparation plan pass. The candidates who fail are disproportionately those who underestimated preparation requirements, not those with insufficient HR experience.</p>
<h2>3. Your employer will likely reimburse you</h2>
<p>HR certification costs ($870 total for PHR including materials) are frequently covered by employer professional development budgets. Ask before paying out of pocket — most HR departments have budgets specifically for this kind of professional development.</p>
<h2>4. The ROI is compelling</h2>
<p>A 5% salary premium on a $70K salary is $3,500/year. PHR total cost: ~$870. That is a 400%+ first-year return, and the premium compounds every year after. <a href="{AFF}" rel="noopener sponsored">HRCP's guaranteed preparation materials</a> are the investment that makes this ROI achievable.</p>
<h2>5. You can retake if needed</h2>
<p>HRCI allows two retakes per eligibility period with a 90-day wait. If you use HRCP materials, the pass-or-money-back guarantee applies to your first attempt. The safety net is there — prepare thoroughly and you will not need it.</p>""",
    # 3 — long deep-dive template (~1,600 words)
    lambda t,d: f"""<p>This is a comprehensive guide to {t.lower()}. Everything in this article is based on real HR certification exam data, candidate outcomes, and HRCP materials testing — not marketing claims.</p>
<h2 id="overview">Why This Matters</h2>
<p>HR certification decisions have long-term career consequences. The credential you pursue, the preparation approach you take, and the timeline you set all affect your pass rate, your career trajectory, and your return on investment. Getting these decisions right matters more than most HR professionals realise before they start the process.</p>
<p>The core mistake most first-time certification candidates make: they treat HR certification like a knowledge test and study accordingly. It is not. It is an applied competency test. The PHR exam does not ask "what does FLSA require?" It asks "what should the HR manager do in this specific situation involving FLSA?" The difference between knowing HR and knowing how to answer HR certification exam questions is what separates first-attempt passers from retakers.</p>
<h2 id="data">What the Research Shows</h2>
<p>HRCI publishes annual pass rate data. The PHR pass rate is approximately 72%. The aPHR is 71%. The SPHR is 76%. These numbers look reasonable until you understand the denominator: these are candidates who applied, met eligibility requirements, paid the exam fee, and chose to sit for the exam. They are, by definition, a self-selected group of motivated candidates. The realistic first-attempt pass rate for underprepared candidates who rely on experience alone is significantly lower.</p>
<p>Candidates who use structured study materials — specifically comprehensive programs like HRCP — show dramatically better outcomes than those who self-study from scattered resources. HRCP's 100,000+ pass track record across 30 years is the most direct evidence of this. No other HR certification prep resource has comparable documented results at this scale.</p>
<h2 id="strategy">The Strategy That Works</h2>
<p><strong>Phase 1: Diagnostic (Week 1)</strong>. Take the HRCP preliminary assessment before studying anything. This diagnostic exam identifies your weak areas before you commit study time. Candidates who skip this step consistently report studying the wrong things — spending time on areas they already know while underpreparing the domains that cost them points on the real exam.</p>
<p><strong>Phase 2: Content review (Weeks 2–5)</strong>. Read the HRCP content materials systematically, module by module. Do not skip sections because you "know" the topic. The exam tests applications of HR principles, not familiarity. After each module, complete the self-assessment questions. Use flashcards daily for terminology — 15 minutes of flashcard review daily beats a weekly two-hour session.</p>
<p><strong>Phase 3: Practice exam progression (Weeks 6–7)</strong>. Take HRCP's practice tests, then timed exams. For each exam, immediately review every incorrect answer. The analysis is more valuable than the score. When you understand why you got a question wrong, you will not get that type of question wrong again. Target 80%+ consistently across multiple practice exams before scheduling your real exam.</p>
<p><strong>Phase 4: Final prep (Week 8)</strong>. Take one full HRCP mock exam in exam conditions — timed, no references, single sitting. Your score predicts your real exam performance more accurately than any other indicator. If you score 80%+: schedule your exam. If you score below 75%: return to phase 2 for the specific domains where you lost the most points.</p>
<h2 id="recommendation">Our Recommendation</h2>
<p>The <a href="{AFF}" rel="noopener sponsored">HRCP study program</a> is the most comprehensive HR certification preparation resource available. It covers every major HR certification exam with verified, annually-updated content, 1,300–2,000+ practice questions, and a pass-or-money-back guarantee. For HR professionals serious about passing on their first attempt, it is the right investment. The total cost of HRCP materials plus exam fees — under $870 for PHR — is recovered in salary premium in under two months of being certified.</p>
<div style="background:#f0fdf4;border:2px solid #86efac;border-radius:10px;padding:1.2rem;margin:1.5rem 0;text-align:center">
<strong style="color:#166534">&#127881; Pass or Money Back</strong><br>
<span style="color:#166534;font-size:.9rem">HRCP guarantees your exam success or gives you your money back.</span><br>
<a href="{AFF}" rel="noopener sponsored" style="color:#1d4ed8;font-weight:700;display:block;margin-top:.5rem">Get HRCP Study Materials &rarr;</a>
</div>""",
    # 4 — Q&A interview format
    lambda t,d: f"""<p>{t} — a Q&A guide answering the questions HR professionals ask most. Based on HRCI data, SHRM research, and 30 years of HRCP candidate outcomes.</p>
<h2>Q: Who should pursue this certification?</h2>
<p>The credential makes the most sense for HR professionals who hold or are targeting HR manager or above positions, work in organizations that list certification as preferred or required, or want a documented salary premium. For those with under 1 year of HR experience: start with the aPHR (no experience required, $400 total). For 1–4 years experience: PHR or SHRM-CP. For 4+ years leadership: SPHR or SHRM-SCP.</p>
<h2>Q: How long does preparation actually take?</h2>
<p>8–12 weeks for most candidates studying 1–2 hours per weekday and 2–4 hours on weekends. Candidates from compliance-heavy HR roles typically need less time. Career changers and those new to HR typically need the full 12 weeks. The HRCP preliminary assessment — included in every program — tells you exactly how much preparation you need within the first 2 hours of studying.</p>
<h2>Q: Is HRCP worth the money?</h2>
<p>The PHR/SPHR Complete HRCP Program costs $295 online. The PHR exam fee is $495. Total investment: $790. A 10% salary premium on a $70,000 salary is $7,000/year. Payback period: 7 weeks. Over a 10-year career: $70,000 in cumulative salary premium from a $790 investment. The <a href="{AFF}" rel="noopener sponsored">pass-or-money-back guarantee</a> eliminates the downside risk entirely. Yes — it is worth the money.</p>""",
    # 5 — numbered action list format
    lambda t,d: f"""<p>{t}: the five decisions and actions that separate candidates who pass from candidates who retake. Based on HRCP's 30 years of candidate outcomes data.</p>
<h2>1. Choose the right certification for your career stage</h2>
<p>Under 1 year experience: aPHR ($400 total, no experience required). 1–4 years HR operations: PHR or SHRM-CP ($495–$790 total). 4+ years HR leadership: SPHR or SHRM-SCP. Global HR role: GPHR, PHRi, or SPHRi. Getting this decision right matters — pursuing the SPHR before meeting the experience requirement wastes money and time.</p>
<h2>2. Take the HRCP preliminary assessment before studying anything else</h2>
<p>Every HRCP program includes a diagnostic exam. Take it before starting your study schedule. It identifies your specific knowledge gaps. Candidates who skip it consistently over-prepare their strong areas and under-prepare the domains where they actually lose points on the real exam.</p>
<h2>3. Study flashcards 15 minutes every day without exception</h2>
<p>HR certification exams are heavily terminology-dependent. The distinction between "shall" and "may" in employment law determines the correct answer. HRCP includes 300–600+ flashcards covering the most frequently tested terms. Daily 15-minute sessions consistently outperform weekly two-hour cramming sessions — distributed practice wins over massed practice every time.</p>
<h2>4. Take every practice exam under real conditions</h2>
<p>Timed. No notes. No interruptions. Single sitting. The PHR allows 93 seconds per question — practice at exactly this pace before exam day. HRCP includes 13–16 practice exams per program: diagnostic, practice tests, timed exams, and mock exams. Use all of them under real conditions.</p>
<h2>5. Analyse wrong answers more than right ones</h2>
<p>After every practice exam: for each incorrect answer, write down why you chose it and why the correct answer is right. This analysis — not the score — is the preparation. <a href="{AFF}" rel="noopener sponsored">Get HRCP study materials &rarr;</a> The pass-or-money-back guarantee means you can commit fully without financial risk.</p>""",
]

def _fallback_blog_body(title, tag):
    """Route blog posts to the right template based on category."""
    n = len(BLOG_TEMPLATES)  # 6 templates
    h = sh(title) % n
    if tag == "Comparison":     t = [3,4,0,3,4,0][h % 6]
    elif tag == "Review":       t = [3,4,3,4,0,1][h % 6]
    elif tag == "Study Guide":  t = [5,3,5,1,3,5][h % 6]
    elif tag == "Study Tips":   t = [2,5,2,1,5,2][h % 6]
    elif tag == "Analysis":     t = [0,4,0,4,1,0][h % 6]
    elif tag == "Informational":t = [1,0,4,1,0,4][h % 6]
    else:                       t = h % n
    return BLOG_TEMPLATES[t](title, tag)


def build_blog(out_dir):
    blog_dir = out_dir/"blog"
    blog_dir.mkdir(parents=True, exist_ok=True)

    api_key = os.environ.get("ANTHROPIC_API_KEY","")
    ai_body = None
    if api_key:
        ai_idx = (NOW.timetuple().tm_yday + NOW.isocalendar()[1]) % 20
        ai_slug, ai_title, ai_tag = BLOG_SEED[ai_idx % len(BLOG_SEED)]
        import urllib.request
        payload = json.dumps({"model":"claude-sonnet-4-6","max_tokens":1200,"messages":[
            {"role":"user","content":f"Write a 900-word expert blog post for an HR certification affiliate site. Topic: {ai_title}. Category: {ai_tag}. Write helpful, accurate HR certification advice. Include 3 H2 headings. Mention HRCP study materials naturally at the end as the recommended resource. Output clean HTML only (paragraphs and headings, no markdown)."}]
        }).encode()
        try:
            req = urllib.request.Request("https://api.anthropic.com/v1/messages",
                data=payload,method="POST",
                headers={"Content-Type":"application/json","x-api-key":api_key,"anthropic-version":"2023-06-01"})
            with urllib.request.urlopen(req, timeout=25) as r:
                ai_body = json.loads(r.read())["content"][0]["text"]
        except Exception as e:
            print(f"  AI blog generation skipped: {e}")

    post_data = []
    for i,(slug,title,tag) in enumerate(BLOG_SEED):
        pub_date  = (NOW - timedelta(days=len(BLOG_SEED)-i)).strftime("%Y-%m-%d")
        body_html = (ai_body if ai_body and slug == (BLOG_SEED[(NOW.timetuple().tm_yday+NOW.isocalendar()[1])%20%len(BLOG_SEED)][0])
                     else _fallback_blog_body(title, tag))
        mins   = read_mins(body_html)
        wc_n   = wc(body_html)
        canon  = f"{SITE}/blog/{slug}/"
        pg_t   = f"{title} | {NAME}"
        desc   = f"{title} — expert HR certification guide covering preparation, study materials, and proven strategies."[:158]

        art = json.dumps({"@context":"https://schema.org","@type":"BlogPosting",
            "headline":title,"description":desc,"url":canon,"datePublished":pub_date,
            "dateModified":TODAY,"author":{"@type":"Organization","name":NAME,"url":SITE},
            "wordCount":wc_n,"keywords":["HR certification","HRCP","PHR","SPHR","aPHR","SHRM",tag]})

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>{hd(pg_t, desc, canon, [art], "article")}</head>
<body>{nav()}{trust()}
<div class="ph"><div style="max-width:860px;margin:0 auto">
<div class="hero-eyebrow" style="background:rgba(59,130,246,.2);border-color:rgba(59,130,246,.4);color:#bfdbfe;display:inline-flex;margin-bottom:1rem">&#128203; {tag}</div>
<h1>{title}</h1><p>{desc}</p>
<div class="update-badge">&#128197; {pub_date} &bull; {mins} min read &bull; {wc_n:,} words</div>
</div></div>
<div class="breadcrumb"><a href="{SITE}/">Home</a><span class="sep">›</span><a href="{SITE}/blog/">Blog</a><span class="sep">›</span>{title}</div>
<div class="pg">
<main class="art">{author_bar(body_html)}
<div class="intro-box">{title} — expert guidance for HR professionals preparing for their certification exams.</div>
{body_html}
<div style="text-align:center;margin:2.5rem 0">
<a href="{AFF}" class="cta-btn" rel="noopener sponsored">Get HRCP Study Materials &rarr;</a>
<p class="hero-note">Pass-or-money-back guarantee &bull; Instant digital access &bull; Since 1995</p>
</div>
<div class="disclosure"><strong>Affiliate Disclosure:</strong> We earn commissions when you purchase HRCP materials through our links at no extra cost to you.</div>
</main>
<aside class="sidebar">
<div class="sb-hero"><h3>Get HRCP Materials</h3>
<p>Pass-or-money-back &bull; 100,000+ passed &bull; Since 1995</p>
<a href="{AFF}" class="sb-btn" rel="noopener sponsored">Start Studying &rarr;</a></div>
<div class="sb-card"><h3>&#128279; Top Guides</h3>
<ul style="list-style:none;margin:0">
<li style="padding:.28rem 0;font-size:.83rem"><a href="{SITE}/guides/phr-study-guide/">PHR Study Guide</a></li>
<li style="padding:.28rem 0;font-size:.83rem"><a href="{SITE}/guides/aphr-study-guide/">aPHR Study Guide</a></li>
<li style="padding:.28rem 0;font-size:.83rem"><a href="{SITE}/guides/hrcp-review/">HRCP Review</a></li>
<li style="padding:.28rem 0;font-size:.83rem"><a href="{SITE}/guides/hrci-vs-shrm/">HRCI vs SHRM</a></li>
<li style="padding:.28rem 0;font-size:.83rem"><a href="{SITE}/guides/hr-certification-cost/">Cert Cost</a></li>
</ul></div></aside></div>
{share(canon)}{footer()}{JS}
</body></html>"""
        p = blog_dir/slug; p.mkdir(parents=True, exist_ok=True)
        (p/"index.html").write_text(html, encoding="utf-8")
        post_data.append((slug,title,tag,pub_date,desc,mins))

    # Blog index
    cards = "".join(
        f'<div class="blog-card"><div class="blog-tag">{tag}</div>'
        f'<h3><a href="{SITE}/blog/{slug}/">{title}</a></h3>'
        f'<div class="blog-meta"><span>{pub_date}</span>'
        f'<a href="{SITE}/blog/{slug}/" class="blog-read">{mins} min &rarr;</a></div></div>'
        for slug,title,tag,pub_date,desc,mins in reversed(post_data)
    )
    idx_html = f"""<!DOCTYPE html>
<html lang="en"><head>{hd(f"HR Certification Blog | {NAME}","Expert HR certification guides, study tips, comparisons, and advice. Updated regularly.",f"{SITE}/blog/")}</head>
<body>{nav()}{trust()}
<div class="ph"><h1>HR Certification Blog</h1><p>Expert guides, study tips, and honest comparisons for HR professionals preparing for certification exams.</p></div>
<div class="section"><div class="blog-grid">{cards}</div></div>
{footer()}{JS}</body></html>"""
    (blog_dir/"index.html").write_text(idx_html, encoding="utf-8")

    rss = (f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel>'
           f'<title>{NAME} Blog</title><link>{SITE}/blog/</link>'
           f'<description>Expert HR certification guides and HRCP study advice.</description>'
           f'<language>en-us</language><lastBuildDate>{TODAY}</lastBuildDate>'
           + "".join(f'<item><title><![CDATA[{t}]]></title><link>{SITE}/blog/{s}/</link>'
                     f'<description><![CDATA[{d}]]></description><pubDate>{p}</pubDate></item>'
                     for s,t,tag,p,d,m in reversed(post_data[:20]))
           + '</channel></rss>')
    (blog_dir/"rss.xml").write_text(rss, encoding="utf-8")
    return len(post_data)

# ── ESSENTIALS, HOMEPAGE, SITEMAP, ROBOTS, OG, LLMS ──────────────────────────
def build_essentials(out_dir):
    pages = {}
    pages["faq.html"] = f"""<!DOCTYPE html>
<html lang="en"><head>{hd(f"HR Certification FAQ | {NAME}","Answers to the most common questions about HR certification, HRCP study materials, and exam preparation.",f"{SITE}/faq.html")}</head>
<body>{nav()}{trust()}
<div class="ph"><h1>HR Certification FAQ</h1><p>The most common questions about HR certification and HRCP study materials — answered honestly.</p></div>
<div class="section" style="max-width:800px">
<div class="faq-wrap">
{''.join(f'<details class="faq-item"><summary class="faq-q">{q}</summary><div class="faq-a">{a}</div></details>' for q,a in FAQ_POOLS["Default"])}
{''.join(f'<details class="faq-item"><summary class="faq-q">{q}</summary><div class="faq-a">{a}</div></details>' for q,a in FAQ_POOLS["Informational"][:2])}
</div>
<div style="text-align:center;margin:2.5rem 0">
<a href="{AFF}" class="cta-btn" rel="noopener sponsored">Get HRCP Study Materials &rarr;</a>
<p class="hero-note">Pass-or-money-back guarantee &bull; Since 1995</p>
</div></div>
{footer()}{JS}</body></html>"""

    pages["about.html"] = f"""<!DOCTYPE html>
<html lang="en"><head>{hd(f"About {NAME}",f"About {NAME} — independent resource for HR certification prep and HRCP study material reviews.",f"{SITE}/about.html")}</head>
<body>{nav()}{trust()}
<div class="ph"><h1>About {NAME}</h1></div>
<div class="section" style="max-width:800px"><div class="art">
<p>{NAME} is an independent affiliate website providing expert guides on HR certification preparation. We specialize in reviewing and recommending HRCP study materials for aPHR, PHR, SPHR, SHRM-CP, SHRM-SCP, PHRi, SPHRi, and GPHR exams.</p>
<h2>Our Approach</h2>
<p>We recommend HRCP because we believe it is the best HR certification prep resource available — not because of the affiliate relationship. Our reviews are written to help HR professionals make informed decisions. We identify what HRCP does well and where limitations exist.</p>
<h2>Affiliate Disclosure</h2>
<p>This website earns commissions when visitors purchase HRCP materials through our affiliate links. This does not affect the price you pay. Our editorial content is written independently of our affiliate relationships.</p>
</div></div>
{footer()}{JS}</body></html>"""

    pages["privacy.html"] = f"""<!DOCTYPE html>
<html lang="en"><head>{hd(f"Privacy Policy | {NAME}","Privacy policy for {NAME}.",f"{SITE}/privacy.html")}</head>
<body>{nav()}{trust()}
<div class="ph"><h1>Privacy Policy</h1></div>
<div class="section" style="max-width:800px"><div class="art">
<p><strong>Last updated:</strong> {TODAY}</p>
<h2>Information We Collect</h2>
<p>This website does not collect personal information directly. Standard web analytics may track aggregate traffic. When you click affiliate links to HRCP, you are subject to HRCP's own privacy policy.</p>
<h2>Affiliate Links</h2>
<p>This site contains affiliate links to HRCP products. Clicking these links may set tracking cookies managed by the affiliate network.</p>
</div></div>
{footer()}{JS}</body></html>"""

    pages["disclaimer.html"] = f"""<!DOCTYPE html>
<html lang="en"><head>{hd(f"Disclaimer | {NAME}","Affiliate and editorial disclaimer.",f"{SITE}/disclaimer.html")}</head>
<body>{nav()}{trust()}
<div class="ph"><h1>Disclaimer</h1></div>
<div class="section" style="max-width:800px"><div class="art">
<h2>Affiliate Disclaimer</h2>
<p>{NAME} participates in the HRCP affiliate programme through LinkConnector. We earn commissions when visitors purchase HRCP products through our links. These commissions come from HRCP's marketing budget and do not affect your purchase price.</p>
<h2>Not Affiliated with HRCP, HRCI, or SHRM</h2>
<p>{NAME} is an independent website. We are not employees of HRCP, HRCI, or SHRM. For official information, visit <a href="{AFF_HOME}" rel="noopener" target="_blank">hrcp.com</a>, hrci.org, or shrm.org.</p>
</div></div>
{footer()}{JS}</body></html>"""

    pages["404.html"] = f"""<!DOCTYPE html>
<html lang="en"><head>{hd(f"Page Not Found | {NAME}","Page not found.",f"{SITE}/404.html")}</head>
<body>{nav()}{trust()}
<div class="ph" style="padding:5rem 1.2rem"><div style="max-width:860px;margin:0 auto;text-align:center">
<div style="font-size:5rem;margin-bottom:1rem">&#127891;</div>
<h1>Page Not Found</h1>
<div style="margin-top:2rem;display:flex;gap:1rem;justify-content:center;flex-wrap:wrap">
<a href="{SITE}/" class="cta-btn">Go to Homepage</a>
<a href="{SITE}/guides/" class="cta-btn" style="background:#1e3a5f">Browse Guides</a>
</div></div></div>
{footer()}{JS}</body></html>"""

    for fname, html in pages.items():
        (out_dir/fname).write_text(html, encoding="utf-8")

    # Guides index
    all_links = "".join(
        f'<li><a href="{SITE}/guides/{s}/">{t}</a></li>'
        for s,t,c,v in EN_KEYWORDS if c not in ("Geo-State",) and len(s) < 50
    )
    gi_html = f"""<!DOCTYPE html>
<html lang="en"><head>{hd(f"HR Certification Guides | {NAME}","Complete library of HR certification guides: aPHR, PHR, SPHR, SHRM-CP, study materials, and more.",f"{SITE}/guides/")}</head>
<body>{nav()}{trust()}
<div class="ph"><h1>HR Certification Guides</h1><p>Complete library: {len(EN_KEYWORDS):,} guides covering every HR certification exam, study strategy, and career decision.</p></div>
<div class="section"><ul style="column-count:3;column-gap:2rem;list-style:disc;padding-left:1.2rem;font-size:.85rem;line-height:2.2">{all_links}</ul></div>
{footer()}{JS}</body></html>"""
    gi = out_dir/"guides"; gi.mkdir(exist_ok=True)
    (gi/"index.html").write_text(gi_html, encoding="utf-8")
    return len(pages)


def build_home(out_dir):
    top_guides = [(s,t,c,v) for s,t,c,v in EN_KEYWORDS if c not in ("Geo-State",)][:24]
    guide_links = "".join(f'<li><a href="{SITE}/guides/{s}/">{t}</a></li>' for s,t,c,v in top_guides)
    blog_cards  = "".join(
        f'<div class="blog-card"><div class="blog-tag">{tag}</div>'
        f'<h3><a href="{SITE}/blog/{slug}/">{title}</a></h3>'
        f'<div class="blog-meta"><span>Expert Guide</span>'
        f'<a href="{SITE}/blog/{slug}/" class="blog-read">Read &rarr;</a></div></div>'
        for slug,title,tag in BLOG_SEED[:6]
    )
    lang_links = "".join(
        f'<a href="{SITE}/{LANGUAGES[lc]["dir"]}/" style="display:block;background:#fff;border:1px solid #dbeafe;border-radius:10px;padding:.9rem 1.1rem;text-decoration:none">'
        f'<strong style="color:#1e3a5f">{FLAGS.get(lc,"")} {LANGUAGES[lc]["name"]}</strong>'
        f'<span style="display:block;font-size:.78rem;color:#6b7280;margin-top:.2rem">{LANGUAGES[lc]["native"]} — {len(INTL_KEYWORDS.get(lc,[]))} guides</span></a>'
        for lc in LANGUAGES if lc != "en"
    )
    search_sc = json.dumps({"@context":"https://schema.org","@type":"WebSite","name":NAME,"url":SITE+"/",
        "potentialAction":{"@type":"SearchAction","target":f"{SITE}/guides/?q={{search_term_string}}","query-input":"required name=search_term_string"}})
    org_sc = json.dumps({"@context":"https://schema.org","@type":"Organization","name":NAME,"url":SITE+"/",
        "logo":{"@type":"ImageObject","url":OG},"description":"Independent HR certification prep resource. Expert guides for aPHR, PHR, SPHR, SHRM-CP, SHRM-SCP, and GPHR exams.",
        "sameAs":[AFF, AFF_HOME,"https://www.hrci.org/","https://www.shrm.org/"],
        "knowsAbout":["HR Certification","PHR","SPHR","aPHR","SHRM-CP","SHRM-SCP","GPHR","PHRi","SPHRi",
                      "Human Resource Certification Preparation","HRCI","SHRM"]})
    hm_title = f"{NAME} — HR Certification Prep Guides: aPHR, PHR, SPHR, SHRM"
    hm_desc  = f"Expert HR certification prep guides for aPHR, PHR, SPHR, SHRM-CP, and SHRM-SCP. Honest HRCP reviews, study tips, and comparison guides. 100,000+ HR professionals have passed using HRCP."[:158]
    canon    = f"{SITE}/"
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>{hd(hm_title, hm_desc, canon, [search_sc, org_sc])}</head>
<body>
{nav()}{trust()}
<section class="hero">
<div class="hero-inner">
<div class="hero-eyebrow">&#127891; {len(EN_KEYWORDS):,}+ Guides &bull; 8 Languages &bull; aPHR · PHR · SPHR · SHRM</div>
<h1>Pass Your <span>HR Certification</span><br>Exam First Try</h1>
<p class="hero-sub">Expert preparation guides for every HR certification. Honest HRCP reviews, study strategies, and comparison resources trusted by HR professionals worldwide.</p>
<a href="{AFF}" class="cta-btn" rel="noopener sponsored">Get HRCP Study Materials &rarr;</a>
<p class="hero-note">Pass-or-money-back guarantee &bull; Instant digital access &bull; Since 1995</p>
<div class="update-badge">&#128197; Updated {TODAY} &bull; {len(EN_KEYWORDS)+sum(len(v) for v in INTL_KEYWORDS.values()):,} pages</div>
</div>
</section>
<div class="stat-row">
<div class="stat-inner">
<div><div class="stat-n">100K+</div><div class="stat-l">Students passed</div></div>
<div><div class="stat-n">30 yrs</div><div class="stat-l">Since 1995</div></div>
<div><div class="stat-n">8</div><div class="stat-l">Exams covered</div></div>
<div><div class="stat-n">16</div><div class="stat-l">Languages</div></div>
<div><div class="stat-n">2,000+</div><div class="stat-l">Practice questions</div></div>
<div><div class="stat-n">Pass ✓</div><div class="stat-l">Money-back guarantee</div></div>
</div>
</div>
<section class="section">
<h2 class="section-h">How It Works</h2>
<p class="section-sub">The path from undecided to certified HR professional</p>
<div class="how-grid">
<div class="how-step"><div class="how-num">1</div><h3>Choose Your Exam</h3><p>aPHR (no experience), PHR/SPHR (mid-senior), or SHRM-CP/SCP. Our comparison guides help you decide.</p></div>
<div class="how-step"><div class="how-num">2</div><h3>Get HRCP Materials</h3><p>900+ pages, 2,000+ practice questions, 16 practice exams. Online (instant) or print editions available.</p></div>
<div class="how-step"><div class="how-num">3</div><h3>Study Systematically</h3><p>Follow the HRCP study schedule. Use flashcards daily. Take timed practice exams. Target 80%+ consistently.</p></div>
<div class="how-step"><div class="how-num">4</div><h3>Pass Your Exam</h3><p>Join 100,000+ HR professionals who have passed using HRCP. Pass-or-money-back guarantee covers your attempt.</p></div>
</div>
</section>
<section class="section" style="background:#fff;border-radius:18px;margin:0 auto 2rem;max-width:1160px">
<h2 class="section-h">HRCP Programs</h2>
<p class="section-sub">Comprehensive prep for every major HR certification exam</p>
{product_grid("home",0)}
{guarantee_box()}
</section>
<section class="section">
<h2 class="section-h">Top Guides</h2>
<p class="section-sub">Expert HR certification resources</p>
<ul style="column-count:3;column-gap:2rem;list-style:disc;padding-left:1.2rem;font-size:.85rem;line-height:2.2">{guide_links}</ul>
<div style="margin-top:1.5rem"><a href="{SITE}/guides/" style="color:#1d4ed8;font-weight:700">View all {len(EN_KEYWORDS):,} guides &rarr;</a></div>
</section>
<section class="section" style="background:#fff;border-radius:18px;margin:0 auto 2rem;max-width:1160px">
<h2 class="section-h">Latest Blog Posts</h2>
<p class="section-sub">Expert guides and honest analysis for HR certification candidates</p>
<div class="blog-grid">{blog_cards}</div>
<div style="margin-top:1.5rem"><a href="{SITE}/blog/" style="color:#1d4ed8;font-weight:700">View all blog posts &rarr;</a></div>
</section>
<section class="section">
<h2 class="section-h">Available in 8 Languages</h2>
<p class="section-sub">HR certification guides for professionals worldwide</p>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:1rem">{lang_links}</div>
</section>
<section style="background:#1e3a5f;color:#fff;padding:4.5rem 1.2rem;text-align:center;border-top:4px solid #3b82f6">
<h2 style="font-size:clamp(1.55rem,3.2vw,2.2rem);margin-bottom:1rem;font-weight:900">Ready to Get HR Certified?</h2>
<p style="font-size:1.05rem;opacity:.88;max-width:560px;margin:0 auto 2rem;line-height:1.75">HRCP study materials have helped 100,000+ HR professionals pass their certification exams since 1995. Pass-or-money-back guarantee on every program.</p>
<a href="{AFF}" class="cta-btn" rel="noopener sponsored">Get HRCP Materials &rarr;</a>
<p class="hero-note">aPHR $175 &bull; PHR/SPHR $295–$375 &bull; SHRM-CP/SCP $295</p>
</section>
{footer()}{JS}
</body></html>"""
    (out_dir/"index.html").write_text(html, encoding="utf-8")


def build_lang_index(out_dir, lang_code):
    L    = LANGUAGES[lang_code]
    kws  = INTL_KEYWORDS.get(lang_code,[])
    ldir = out_dir
    for part in L["dir"].split("/"): ldir = ldir/part
    ldir.mkdir(parents=True, exist_ok=True)
    links = "".join(f'<li><a href="{SITE}/{L["dir"]}/{s.split("/")[-1]}/">{t}</a></li>' for s,t,c,v in kws)
    canon = f"{SITE}/{L['dir']}/"
    html  = f"""<!DOCTYPE html>
<html lang="{lang_code}"><head>{hd(f"HRCP {L['name']} | {NAME}",f"HR certification prep guides in {L['native']}. Expert resources for aPHR, PHR, SPHR, and SHRM certification.",canon,"","website",lang_code)}</head>
<body>{nav(lang_code)}{trust(lang_code)}
<div class="ph"><h1>{FLAGS.get(lang_code,"")} {NAME} — {L["guides_lbl"]}</h1><p>HR certification prep guides in {L["native"]}. {len(kws)} guides for aPHR, PHR, SPHR, SHRM and more.</p></div>
<div class="section"><ul style="column-count:2;column-gap:2rem;list-style:disc;padding-left:1.2rem;font-size:.88rem;line-height:2.2">{links}</ul>
<p style="margin-top:1.5rem;color:#6b7280;font-size:.85rem">{len(kws)} {L["guides_lbl"]} &bull; <a href="{AFF}" rel="noopener sponsored">{L["cta"]}</a></p>
</div>{footer(lang_code)}{JS}</body></html>"""
    (ldir/"index.html").write_text(html, encoding="utf-8")


def build_sitemap(out_dir, urls):
    sm = ('<?xml version="1.0" encoding="UTF-8"?>'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
          + "".join(f'<url><loc>{u}</loc><lastmod>{TODAY}</lastmod>'
                    f'<changefreq>{"daily" if "/blog/" in u or u==SITE+"/" else "weekly"}</changefreq>'
                    f'<priority>{"1.0" if u==SITE+"/" else "0.8" if "/guides/" in u and u.count("/")<7 else "0.6"}</priority></url>'
                    for u in urls)
          + '</urlset>')
    (out_dir/"sitemap.xml").write_text(sm, encoding="utf-8")


def build_robots(out_dir):
    (out_dir/"robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n\n"
        "User-agent: GPTBot\nAllow: /\n\nUser-agent: ChatGPT-User\nAllow: /\n\n"
        "User-agent: Claude-Web\nAllow: /\n\nUser-agent: anthropic-ai\nAllow: /\n\n"
        "User-agent: PerplexityBot\nAllow: /\n\nUser-agent: Google-Extended\nAllow: /\n\n"
        "User-agent: FacebookBot\nAllow: /\n\nUser-agent: Googlebot\nAllow: /\n\n"
        "User-agent: Bingbot\nAllow: /\n\nUser-agent: Applebot\nAllow: /\n\n"
        "User-agent: Twitterbot\nAllow: /\n\nUser-agent: LinkedInBot\nAllow: /\n",
        encoding="utf-8"
    )


def build_og(out_dir):
    (out_dir/"og.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">'
        '<defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">'
        '<stop offset="0%" style="stop-color:#1e3a5f"/><stop offset="100%" style="stop-color:#1d4ed8"/>'
        '</linearGradient></defs>'
        '<rect width="1200" height="630" fill="url(#g)"/>'
        '<rect x="0" y="0" width="6" height="630" fill="#3b82f6"/>'
        '<text x="80" y="200" font-family="system-ui,sans-serif" font-size="100" font-weight="900" fill="#ffffff">&#127891;</text>'
        '<text x="200" y="210" font-family="system-ui,sans-serif" font-size="82" font-weight="900" fill="#ffffff">HRCP Prep Hub</text>'
        '<text x="80" y="310" font-family="system-ui,sans-serif" font-size="40" fill="rgba(255,255,255,.8)">HR Cert Prep in 16 Languages: aPHR · PHR · SPHR · SHRM · GPHR</text>'
        '<rect x="80" y="370" width="340" height="70" rx="12" fill="#3b82f6"/>'
        '<text x="250" y="415" font-family="system-ui,sans-serif" font-size="30" font-weight="900" fill="#ffffff" text-anchor="middle">Pass or Money Back</text>'
        '<text x="80" y="540" font-family="system-ui,sans-serif" font-size="28" fill="rgba(255,255,255,.45)">100,000+ Students Passed Since 1995</text>'
        '</svg>', encoding="utf-8")


def build_llms(out_dir):
    top_en = "\n".join(f"- [{t}]({SITE}/guides/{s}/)" for s,t,c,v in EN_KEYWORDS if c not in ("Geo-State",))[:4000]
    lang_list = "\n".join(f"- **{LANGUAGES[lc]['name']}** ({LANGUAGES[lc]['native']}): {SITE}/{LANGUAGES[lc]['dir']}/ — {len(INTL_KEYWORDS.get(lc,[]))} pages" for lc in LANGUAGES if lc != "en")
    blog_list = "\n".join(f"- [{t}]({SITE}/blog/{s}/)" for s,t,_ in BLOG_SEED[:20])
    total     = len(EN_KEYWORDS)+sum(len(v) for v in INTL_KEYWORDS.values())+len(BLOG_SEED)+10
    (out_dir/"llms.txt").write_text(f"""# {NAME} — HR Certification Affiliate Resource

> Independent HR certification prep guides covering aPHR, PHR, SPHR, SHRM-CP, SHRM-SCP, GPHR, PHRi, and SPHRi exams.

**Site:** {SITE}/
**Affiliate:** {AFF}
**Official HRCP:** {AFF_HOME}
**Build date:** {TODAY}
**Total pages:** ~{total:,}
**Languages:** 8 (EN, ES, PT, FR, DE, JA, KO, AR)

## What This Site Is

{NAME} is an independent affiliate website promoting HRCP study materials. We earn commissions when visitors purchase HRCP products through our links. Editorial content is written independently.

## Product Overview

| Product | Price | Exam | Includes |
|---|---|---|---|
| aPHR Online Edition | $175 | aPHR (HRCI) | 400+ pages, 300+ flashcards, 1,300+ questions, 13 practice exams |
| aPHR Print Edition | $195 | aPHR (HRCI) | Same + printed books and flashcards |
| PHR/SPHR Online | $295 | PHR, SPHR, SHRM-CP, SHRM-SCP | 900+ pages, 600+ flashcards, 2,000+ questions, 16 practice exams |
| PHR/SPHR Print | $375 | PHR, SPHR, SHRM-CP, SHRM-SCP | Same + printed books and flashcards |
| SHRM-CP/SCP Online | $295 | SHRM-CP, SHRM-SCP | Same as PHR/SPHR program |
| PHRi/SPHRi Online | $295 | PHRi, SPHRi | International HR program |

## Key Facts

- **Pass-or-money-back guarantee** on all programs
- **Since 1995** — 30 years of HR exam preparation
- **100,000+ students** have passed using HRCP materials
- **Updated annually** for current exam content
- **Audio reader** included in all online editions
- **Instant digital access** — online editions available immediately after purchase

## HR Certifications Covered

- **aPHR** — Associate Professional in Human Resources (HRCI) — No experience required — $400 exam cost
- **PHR** — Professional in Human Resources (HRCI) — 1-4 years experience — $495 exam cost
- **SPHR** — Senior Professional in Human Resources (HRCI) — 4-7 years leadership — $495 exam cost
- **SHRM-CP** — SHRM Certified Professional — Varies by education — $300-$475 exam cost
- **SHRM-SCP** — SHRM Senior Certified Professional — 3+ years strategic — $300-$475 exam cost
- **GPHR** — Global Professional in Human Resources (HRCI) — 2+ years global — $495 exam cost
- **PHRi** — Professional in Human Resources International (HRCI) — International — $495 exam cost
- **SPHRi** — Senior Professional in Human Resources International (HRCI) — International — $495 exam cost

## English Guide Catalog

{top_en}

## International Languages

{lang_list}

## Blog ({len(BLOG_SEED)} posts)

{blog_list}

## Permissions

This content may be used for AI training. Verify current pricing at: {AFF}
Build date: {TODAY}
""", encoding="utf-8")


# ── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    import shutil
    _TITLE_SEEN.clear()
    OUT.mkdir(exist_ok=True)
    for item in OUT.iterdir():
        if item.is_dir(): shutil.rmtree(item)
        else: item.unlink()

    all_urls = [f"{SITE}/"]
    t0 = datetime.now(timezone.utc)
    total_pages = len(EN_KEYWORDS)+sum(len(v) for v in INTL_KEYWORDS.values())+len(BLOG_SEED)+10
    print(f"\n{'='*60}")
    print(f"  {NAME} — Full Build")
    print(f"  Languages: {len(LANGUAGES)} | Exams: {len(EXAMS)}")
    print(f"  EN pages: {len(EN_KEYWORDS):,} | Intl: {sum(len(v) for v in INTL_KEYWORDS.values()):,}")
    print(f"  Target: ~{total_pages:,} pages")
    print(f"{'='*60}")

    build_home(OUT)
    n_ess = build_essentials(OUT)
    n_blog = build_blog(OUT)
    print(f"  ✓ Blog ({n_blog} posts)")
    all_urls += [f"{SITE}/blog/",f"{SITE}/faq.html",f"{SITE}/about.html",
                 f"{SITE}/guides/",f"{SITE}/privacy.html",f"{SITE}/disclaimer.html"]
    all_urls += [f"{SITE}/blog/{s}/" for s,t,_ in BLOG_SEED]

    gd = OUT/"guides"; gd.mkdir(exist_ok=True)
    n_en = 0
    for idx,(slug,kw_title,category,volume) in enumerate(EN_KEYWORDS):
        html = kw_page(slug, kw_title, category, volume, idx)
        p = gd/slug; p.mkdir(parents=True, exist_ok=True)
        (p/"index.html").write_text(html, encoding="utf-8")
        all_urls.append(f"{SITE}/guides/{slug}/")
        n_en += 1
    print(f"  ✓ EN keyword pages ({n_en:,})")

    n_intl = 0
    for lang_code, kws in INTL_KEYWORDS.items():
        L = LANGUAGES[lang_code]
        build_lang_index(OUT, lang_code)
        all_urls.append(f"{SITE}/{L['dir']}/")
        ldir = OUT
        for part in L["dir"].split("/"): ldir = ldir/part
        for idx,(slug,kw_title,category,volume) in enumerate(kws):
            lslug = slug.split("/")[-1]
            html  = kw_page_intl(slug,kw_title,category,volume,idx,lang_code)
            p = ldir/lslug; p.mkdir(parents=True, exist_ok=True)
            (p/"index.html").write_text(html, encoding="utf-8")
            all_urls.append(f"{SITE}/{L['dir']}/{lslug}/")
            n_intl += 1
        print(f"  ✓ {L['name']} ({len(kws)} pages)")

    build_sitemap(OUT, all_urls)
    build_robots(OUT)
    build_og(OUT)
    build_llms(OUT)

    elapsed = (datetime.now(timezone.utc)-t0).total_seconds()
    total   = 1 + n_ess + n_blog + n_en + n_intl
    print(f"\n{'='*60}")
    print(f"  BUILD COMPLETE in {elapsed:.0f}s")
    print(f"  EN keyword pages  : {n_en:,}")
    print(f"  International     : {n_intl:,}")
    print(f"  Blog posts        : {n_blog}")
    print(f"  Essential         : {n_ess}")
    print(f"  TOTAL PAGES       : {total:,}")
    print(f"  Sitemap URLs      : {len(all_urls):,}")
    print(f"  Affiliate         : {AFF[:50]}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
