
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
import logging

TOKEN = "6891860052:AAH_0MsLYUKpALBUyYUHtawqwDXYQi9RXjM"
PORT = 5000  

app = Flask(__name__)
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
computer_specializations = [
    "🖥 هندسة البرمجيات",
    "💻 علوم الحاسوب",
    "🌐 تقنية المعلومات",
    "🔐 أمن المعلومات",
    "🌐 تصميم وتطوير المواقع",
    "🤖 الذكاء الاصطناعي",
    "📊 تحليل البيانات",
    "📱 تطوير تطبيقات الجوال",
    "🌐 هندسة الشبكات",
    "🚀 منصة المشاريع"
]
specializations_details = {
    "🖥 هندسة البرمجيات": "هل تحلم بتطوير برامج قوية وموثوقة؟ ...",
    "💻 علوم الحاسوب": "هل ترغب في استكشاف أسرار الحوسبة والتكنولوجيا؟ ...",
    "🌐 تقنية المعلومات": "هل تهتم بالتكنولوجيا وكيفية استخدامها لدعم المؤسسات ...",
    "🔐 أمن المعلومات": "هل تهتم بحماية البيانات والمعلومات الحساسة ...",
    "🌐 تصميم وتطوير المواقع": "هل ترغب في بناء مواقع ويب جذابة ومتجاوبة ...",
    "🤖 الذكاء الاصطناعي": "هل تثيرك تقنية الذكاء الاصطناعي وتأثيره على حياتنا اليومية؟ ...",
    "📊 تحليل البيانات": "هل تحب التحليل الإحصائي واستخراج الأفكار من البيانات؟ ...",
    "📱 تطوير تطبيقات الجوال": "هل ترغب في تطوير تطبيقات متنقلة لمنصات مختلفة؟ ...",
    "🌐 هندسة الشبكات": "هل ترغب في فهم وبناء البنية التحتية لالشبكات؟",
}

motivational_messages = {
    "🖥 هندسة البرمجيات": "🚀 لنبدأ رحلة بناء البرمجيات المستقبلية! اختر تخصصك وابدأ الاستكشاف.",
    "💻 علوم الحاسوب": "🔍 استكشف عالم الحوسبة وتكنولوجيا المعلومات معنا. اختر وابدأ رحلتك الآن!",
    "🌐 تقنية المعلومات": "💡 دعم المؤسسات بالتكنولوجيا. اختر تخصصك وكن جزءًا من التحول الرقمي.",
    "🔐 أمن المعلومات": "🛡️ حماية البيانات هي مهمتنا. اختر تخصصك وكن جزءًا من فريق الأمان.",
    "🌐 تصميم وتطوير المواقع": "🌐 بناء مواقع ويب جذابة واستجابية. اختر تخصصك وابدأ رحلة التصميم.",
    "🤖 الذكاء الاصطناعي": "🧠 استكشف عالم الذكاء الاصطناعي وتأثيره على حياتنا. اختر وكن جزءًا من المستقبل.",
    "📊 تحليل البيانات": "📈 حول البيانات إلى أفكار. اختر تخصصك واستمتع برحلة التحليل الإحصائي.",
    "📱 تطوير تطبيقات الجوال": "📱 ابدأ في بناء تطبيقات متنقلة رائعة. اختر تخصصك وابدأ رحلة التطوير.",
    "🌐 هندسة الشبكات": "🌐 فهم الشبكات وبناء البنية التحتية. اختر تخصصك واستمتع برحلة الهندسة.",
}

team_achievements = {
    "🖥 هندسة البرمجيات": "🏆 تهانينا! فريق هندسة البرمجيات حقق إنجازًا رائعًا في مشروعهم الأخير.",
    "💻 علوم الحاسوب": "🌟 إنجاز فريق علوم الحاسوب ملفت للنظر. تابعوا العمل الرائع!",
    "🌐 تقنية المعلومات": "🚀 إشارة إلى فريق تقنية المعلومات! نجاح مشروعهم يثبت التفوق.",
    "🔐 أمن المعلومات": "🛡️ فريق أمن المعلومات يحقق إنجازًا مهمًا في حماية البيانات.",
    "🌐 تصميم وتطوير المواقع": "🌐 تصميم مواقع رائعة! فريق التطوير يبهرنا دائمًا.",
    "🤖 الذكاء الاصطناعي": "🧠 إنجازات فريق الذكاء الاصطناعي تعكس الابتكار والتفوق.",
    "📊 تحليل البيانات": "📈 فخر لفريق تحليل البيانات! استمروا في العمل الرائع.",
    "📱 تطوير تطبيقات الجوال": "📱 إنجازات فريق تطوير التطبيقات تبرز في عالم التقنية.",
    "🌐 هندسة الشبكات": "🌐 بناء وصيانة الشبكات. إنجازات فريق الهندسة لا تعد ولا تحصى.",
}

# تعريف المشاريع لكل تخصص
projects_per_specialization = {
    "🖥 هندسة البرمجيات": [
        "تطبيق إدارة المشاريع الذكي",
        "منصة تبادل المشاريع للمطورين",
        "تطبيق مشاريع البرمجيات المفتوحة المصدر",
        # ... (أضف المزيد من المشاريع حسب الحاجة)
    ],
    "🚀 منصة المشاريع": [
        "تطبيق إدارة المشاريع الذكي",
        "منصة تبادل المشاريع للمطورين",
        "تطبيق مشاريع البرمجيات المفتوحة المصدر",
        # ... (أضف المزيد من المشاريع حسب الحاجة)
    ],
    # أضف المشاريع لبقية التخصصات
}

def start_command(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(spec, callback_data=f"specialization_{index}")] for index, spec in enumerate(computer_specializations, start=1)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("مرحبًا بك! قم باختيار تخصصك للتعلم أو لانشاء المشاريع:", reply_markup=reply_markup)

# Add the handler
updater.dispatcher.add_handler(CommandHandler('start', start_command))

def specialization_info(update: Update, context: CallbackContext):
    query = update.callback_query
    user_input = query.data

    try:
        specialization_index = int(user_input.split("_")[1])
        specialization = computer_specializations[specialization_index - 1]

        if specialization == "🚀 منصة المشاريع":
            # عرض قائمة المشاريع عند اختيار "منصة المشاريع"
            projects = projects_per_specialization.get(specialization, [])
            if projects:
                message = f"مشاريع {specialization}:\n\n"
                for i, project in enumerate(projects, start=1):
                    message += f"{i}. {project}\n"
            else:
                message = "لا توجد مشاريع متاحة حاليًا."

        else:
            # إضافة معلومات لبقية التخصصات كما هو متعارف عليه
            message = (
                f"معلومات حول {specialization}:\n\n{specializations_details[specialization]}\n\n"
                f"{motivational_messages.get(specialization, '')}\n\n"
                f"{team_achievements.get(specialization, '')}\n\n"
                f"[اضغط هنا](https://wsend.co/967778095893) \n للمزيد من المعلومات"
            )

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

    except (ValueError, IndexError):
        query.edit_message_text("عذرًا، يرجى اختيار رقم صحيح من القائمة.")

# Add the handler
updater.dispatcher.add_handler(CallbackQueryHandler(specialization_info))

def discover_more(update: Update, context: CallbackContext):
    update.message.reply_text('اكتشف المزيد حول البوت وميزاته الإضافية!')

def handle_text_messages(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()

    if 'مرحبًا' in user_message:
        update.message.reply_text('مرحبًا! كيف يمكنني مساعدتك اليوم؟')

# Add the handler
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text_messages))

def upcoming_events(update: Update, context: CallbackContext):
    update.message.reply_text('تعال وانضم إلينا في ورش العمل القادمة! اطلع على التفاصيل [هنا](https://example.com/events)')

def social_media_links(update: Update, context: CallbackContext):
    update.message.reply_text('تابعنا على وسائل التواصلالاجتماعي للحصول على أحدث التحديثات:\n'
                              '[Facebook](https://www.facebook.com/your_page)\n'
                              '[Twitter](https://twitter.com/your_page)\n'
                              '[Instagram](https://www.instagram.com/your_page)')

# Add the handlers
updater.dispatcher.add_handler(CommandHandler('discover_more', discover_more))
updater.dispatcher.add_handler(CommandHandler('upcoming_events', upcoming_events))
updater.dispatcher.add_handler(CommandHandler('social_media_links', social_media_links))

def start_command(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(spec, callback_data=f"specialization_{index}")] for index, spec in enumerate(computer_specializations, start=1)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("مرحبًا بك ماذا تريد أن تنجز ؟:", reply_markup=reply_markup)

    # Send a motivational message based on the selected specialization
    selected_specialization = "🖥 هندسة البرمجيات"  # You need to replace this with the actual selected specialization
    if selected_specialization in motivational_messages:
        update.message.reply_text(motivational_messages[selected_specialization])

if __name__ == "__main__":
    # Start the Bot
    updater.start_polling()
    updater.idle()
