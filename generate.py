import os
import re

BUNDLE = r'''
=== settings.gradle.kts ===
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "NightPlayer"
include(":app")
=== build.gradle.kts ===
plugins {
    id("com.android.application") version "8.5.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.24" apply false
}
=== gradle.properties ===
org.gradle.jvmargs=-Xmx3g -Dfile.encoding=UTF-8
android.useAndroidX=true
android.nonTransitiveRClass=true
kotlin.code.style=official
=== app/build.gradle.kts ===
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.nightplayer.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.nightplayer.app"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.activity:activity-ktx:1.9.0")
    implementation("androidx.recyclerview:recyclerview:1.3.2")
    val media3 = "1.3.1"
    implementation("androidx.media3:media3-exoplayer:$media3")
    implementation("androidx.media3:media3-exoplayer-hls:$media3")
    implementation("androidx.media3:media3-ui:$media3")
    implementation("androidx.media3:media3-session:$media3")
}
=== app/src/main/AndroidManifest.xml ===
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" android:maxSdkVersion="32" />
    <uses-permission android:name="android.permission.READ_MEDIA_VIDEO" />
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.WAKE_LOCK" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_MEDIA_PLAYBACK" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />

    <application
        android:allowBackup="true"
        android:icon="@drawable/ic_launcher"
        android:label="Night Player"
        android:supportsRtl="true"
        android:usesCleartextTraffic="true"
        android:theme="@style/Theme.Night">

        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <activity
            android:name=".PlayerActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:supportsPictureInPicture="true"
            android:resizeableActivity="true"
            android:configChanges="orientation|screenSize|smallestScreenSize|screenLayout|keyboardHidden|uiMode">
            <intent-filter>
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="content" />
                <data android:scheme="file" />
                <data android:scheme="http" />
                <data android:scheme="https" />
                <data android:mimeType="video/*" />
            </intent-filter>
        </activity>

        <service
            android:name=".PlaybackService"
            android:exported="true"
            android:foregroundServiceType="mediaPlayback">
            <intent-filter>
                <action android:name="androidx.media3.session.MediaSessionService" />
            </intent-filter>
        </service>
    </application>
</manifest>
=== app/src/main/res/values/themes.xml ===
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.Night" parent="@android:style/Theme.Material.NoActionBar">
        <item name="android:windowBackground">@android:color/black</item>
        <item name="android:statusBarColor">#0B0F1A</item>
        <item name="android:navigationBarColor">#0B0F1A</item>
        <item name="android:colorAccent">#8C9EFF</item>
        <item name="android:colorPrimary">#121829</item>
    </style>
</resources>
=== app/src/main/res/drawable/ic_launcher.xml ===
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#0B0F1A"
        android:pathData="M0,0h108v108h-108z" />
    <path
        android:fillColor="#232C47"
        android:pathData="M54,14 A40,40 0 1,1 53.9,14 Z" />
    <path
        android:fillColor="#8C9EFF"
        android:pathData="M44,34 L78,54 L44,74 Z" />
</vector>
=== app/src/main/java/com/nightplayer/app/Util.kt ===
package com.nightplayer.app

import android.content.Context
import android.graphics.Color
import android.graphics.drawable.GradientDrawable
import android.net.Uri
import android.util.TypedValue
import android.view.Gravity
import android.widget.TextView
import java.util.Locale

object Night {
    val BG = Color.parseColor("#0B0F1A")
    val SURFACE = Color.parseColor("#121829")
    val CARD = Color.parseColor("#1A2238")
    val CARD2 = Color.parseColor("#232C47")
    val ACCENT = Color.parseColor("#8C9EFF")
    val ACCENT2 = Color.parseColor("#B388FF")
    val TEXT = Color.parseColor("#E6E9F5")
    val MUTED = Color.parseColor("#8A93B2")
}

data class VideoItem(
    val id: Long,
    val uri: Uri,
    val name: String,
    val duration: Long,
    val size: Long,
    val folder: String,
    val dateAdded: Long
)

fun Context.dp(v: Int): Int =
    TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, v.toFloat(), resources.displayMetrics).toInt()

fun Context.roundBg(color: Int, radiusDp: Int): GradientDrawable =
    GradientDrawable().apply {
        setColor(color)
        cornerRadius = dp(radiusDp).toFloat()
    }

fun Context.iconButton(label: String, sizeSp: Int = 20, onClick: () -> Unit): TextView =
    TextView(this).apply {
        this.text = label
        textSize = sizeSp.toFloat()
        setTextColor(Night.TEXT)
        gravity = Gravity.CENTER
        setPadding(dp(12), dp(8), dp(12), dp(8))
        setOnClickListener { onClick() }
    }

fun formatTime(ms: Long): String {
    val total = if (ms < 0) 0 else ms / 1000
    val h = total / 3600
    val m = (total % 3600) / 60
    val s = total % 60
    return if (h > 0) String.format(Locale.US, "%d:%02d:%02d", h, m, s)
    else String.format(Locale.US, "%02d:%02d", m, s)
}

fun formatSize(bytes: Long): String {
    val mb = bytes / 1048576.0
    return if (mb >= 1024) String.format(Locale.US, "%.2f GB", mb / 1024)
    else String.format(Locale.US, "%.0f MB", mb)
}
=== app/src/main/java/com/nightplayer/app/PlaybackService.kt ===
@file:OptIn(androidx.media3.common.util.UnstableApi::class)

package com.nightplayer.app

import android.app.PendingIntent
import android.content.Intent
import androidx.media3.common.AudioAttributes
import androidx.media3.common.C
import androidx.media3.exoplayer.DefaultRenderersFactory
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.session.MediaSession
import androidx.media3.session.MediaSessionService

class PlaybackService : MediaSessionService() {

    private var session: MediaSession? = null

    override fun onCreate() {
        super.onCreate()
        val renderers = DefaultRenderersFactory(this).setEnableDecoderFallback(true)
        val player = ExoPlayer.Builder(this, renderers)
            .setAudioAttributes(
                AudioAttributes.Builder()
                    .setContentType(C.AUDIO_CONTENT_TYPE_MOVIE)
                    .setUsage(C.USAGE_MEDIA)
                    .build(),
                true
            )
            .setHandleAudioBecomingNoisy(true)
            .setWakeMode(C.WAKE_MODE_LOCAL)
            .setSeekBackIncrementMs(10000L)
            .setSeekForwardIncrementMs(10000L)
            .build()

        val intent = Intent(this, PlayerActivity::class.java)
            .addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP)
        val pi = PendingIntent.getActivity(
            this, 0, intent,
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )
        session = MediaSession.Builder(this, player).setSessionActivity(pi).build()
    }

    override fun onGetSession(controllerInfo: MediaSession.ControllerInfo): MediaSession? = session

    override fun onTaskRemoved(rootIntent: Intent?) {
        val p = session?.player
        if (p == null || !p.playWhenReady || p.mediaItemCount == 0) {
            stopSelf()
        }
    }

    override fun onDestroy() {
        session?.let {
            it.player.release()
            it.release()
        }
        session = null
        super.onDestroy()
    }
}
=== app/src/main/java/com/nightplayer/app/MainActivity.kt ===
package com.nightplayer.app

import android.Manifest
import android.app.AlertDialog
import android.content.ContentUris
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.Typeface
import android.media.MediaMetadataRetriever
import android.os.Build
import android.os.Bundle
import android.provider.MediaStore
import android.text.Editable
import android.text.TextWatcher
import android.util.LruCache
import android.util.Size
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import android.widget.FrameLayout
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.OnBackPressedCallback
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import java.util.concurrent.Executors

sealed class Row {
    data class Folder(val name: String, val count: Int, val total: Long) : Row()
    data class Vid(val v: VideoItem) : Row()
}

class RowVH(
    val card: LinearLayout,
    val img: ImageView,
    val icon: TextView,
    val badge: TextView,
    val title: TextView,
    val meta: TextView
) : RecyclerView.ViewHolder(card)

class MainActivity : ComponentActivity() {

    private lateinit var titleView: TextView
    private lateinit var searchBox: EditText
    private lateinit var emptyView: TextView
    private lateinit var recycler: RecyclerView
    private val rowAdapter = RowAdapter()

    private var all: List<VideoItem> = emptyList()
    private var currentFolder: String? = null
    private var showFolders = true
    private var sortMode = 0

    private val prefs by lazy { getSharedPreferences("night", MODE_PRIVATE) }
    private val pool = Executors.newFixedThreadPool(3)
    private val thumbCache = object : LruCache<Long, Bitmap>(80) {}

    private val videoPerm: String
        get() = if (Build.VERSION.SDK_INT >= 33) Manifest.permission.READ_MEDIA_VIDEO
        else Manifest.permission.READ_EXTERNAL_STORAGE

    private val notifLauncher =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { }

    private val permLauncher =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
            if (granted) {
                loadVideos()
                askNotif()
            } else {
                showEmpty("نحتاج إذن الوصول للفيديوهات.\nاضغط هنا لإعطاء الإذن")
            }
        }

    private fun hasPerm() =
        ContextCompat.checkSelfPermission(this, videoPerm) == PackageManager.PERMISSION_GRANTED

    private fun askNotif() {
        if (Build.VERSION.SDK_INT >= 33 &&
            ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS)
            != PackageManager.PERMISSION_GRANTED &&
            !prefs.getBoolean("asked_notif", false)
        ) {
            prefs.edit().putBoolean("asked_notif", true).apply()
            notifLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(Night.BG)
        }

        val bar = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(dp(14), dp(10), dp(6), dp(10))
        }
        titleView = TextView(this).apply {
            text = "Night Player"
            textSize = 22f
            setTypeface(typeface, Typeface.BOLD)
            setTextColor(Night.TEXT)
        }
        bar.addView(titleView, LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f))
        bar.addView(iconButton("🔍") { toggleSearch() })
        bar.addView(iconButton("⇅") { sortDialog() })
        bar.addView(iconButton("🗂") {
            showFolders = !showFolders
            currentFolder = null
            refresh()
            Toast.makeText(this, if (showFolders) "عرض المجلدات" else "عرض كل الفيديوهات", Toast.LENGTH_SHORT).show()
        })
        bar.addView(iconButton("🔗") { urlDialog() })
        root.addView(bar)

        searchBox = EditText(this).apply {
            hint = "ابحث عن فيديو..."
            setHintTextColor(Night.MUTED)
            setTextColor(Night.TEXT)
            textSize = 15f
            maxLines = 1
            isSingleLine = true
            background = roundBg(Night.CARD, 12)
            setPadding(dp(14), dp(10), dp(14), dp(10))
            visibility = View.GONE
            addTextChangedListener(object : TextWatcher {
                override fun afterTextChanged(s: Editable?) { refresh() }
                override fun beforeTextChanged(s: CharSequence?, st: Int, c: Int, a: Int) {}
                override fun onTextChanged(s: CharSequence?, st: Int, b: Int, c: Int) {}
            })
        }
        val sp = LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT)
        sp.setMargins(dp(12), 0, dp(12), dp(6))
        root.addView(searchBox, sp)

        recycler = RecyclerView(this).apply {
            layoutManager = LinearLayoutManager(this@MainActivity)
            adapter = rowAdapter
            clipToPadding = false
            setPadding(0, dp(4), 0, dp(16))
        }
        emptyView = TextView(this).apply {
            textSize = 16f
            gravity = Gravity.CENTER
            setTextColor(Night.MUTED)
            visibility = View.GONE
        }
        val frame = FrameLayout(this)
        frame.addView(recycler, FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT))
        frame.addView(emptyView, FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT))
        root.addView(frame, LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f))
        setContentView(root)

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (searchBox.visibility == View.VISIBLE) {
                    searchBox.setText("")
                    searchBox.visibility = View.GONE
                } else if (currentFolder != null) {
                    currentFolder = null
                    refresh()
                } else {
                    isEnabled = false
                    onBackPressedDispatcher.onBackPressed()
                }
            }
        })

        if (!hasPerm()) permLauncher.launch(videoPerm)
    }

    override fun onResume() {
        super.onResume()
        if (hasPerm()) loadVideos()
    }

    private fun toggleSearch() {
        if (searchBox.visibility == View.VISIBLE) {
            searchBox.setText("")
            searchBox.visibility = View.GONE
        } else {
            searchBox.visibility = View.VISIBLE
            searchBox.requestFocus()
        }
    }

    private fun sortDialog() {
        val items = arrayOf("الأحدث أولاً", "الاسم", "الأكبر حجماً", "الأطول مدة")
        AlertDialog.Builder(this)
            .setTitle("ترتيب حسب")
            .setItems(items) { _, i ->
                sortMode = i
                refresh()
            }.show()
    }

    private fun urlDialog() {
        val input = EditText(this).apply {
            hint = "https://..."
            setSingleLine()
        }
        AlertDialog.Builder(this)
            .setTitle("تشغيل رابط فيديو")
            .setView(input)
            .setPositiveButton("تشغيل") { _, _ ->
                val u = input.text.toString().trim()
                if (u.isNotEmpty()) {
                    startActivity(
                        Intent(this, PlayerActivity::class.java)
                            .putStringArrayListExtra("uris", arrayListOf(u))
                            .putStringArrayListExtra("titles", arrayListOf(u))
                            .putExtra("index", 0)
                    )
                }
            }
            .setNegativeButton("إلغاء", null)
            .show()
    }

    private fun showEmpty(msg: String) {
        emptyView.text = msg
        emptyView.visibility = View.VISIBLE
        emptyView.setOnClickListener {
            if (!hasPerm()) permLauncher.launch(videoPerm)
        }
    }

    private fun loadVideos() {
        pool.execute {
            val list = ArrayList<VideoItem>()
            val proj = arrayOf(
                MediaStore.Video.Media._ID,
                MediaStore.Video.Media.DISPLAY_NAME,
                MediaStore.Video.Media.DURATION,
                MediaStore.Video.Media.SIZE,
                MediaStore.Video.Media.BUCKET_DISPLAY_NAME,
                MediaStore.Video.Media.DATE_ADDED
            )
            try {
                contentResolver.query(
                    MediaStore.Video.Media.EXTERNAL_CONTENT_URI, proj, null, null, null
                )?.use { c ->
                    val iId = c.getColumnIndexOrThrow(MediaStore.Video.Media._ID)
                    val iName = c.getColumnIndexOrThrow(MediaStore.Video.Media.DISPLAY_NAME)
                    val iDur = c.getColumnIndexOrThrow(MediaStore.Video.Media.DURATION)
                    val iSize = c.getColumnIndexOrThrow(MediaStore.Video.Media.SIZE)
                    val iBucket = c.getColumnIndexOrThrow(MediaStore.Video.Media.BUCKET_DISPLAY_NAME)
                    val iDate = c.getColumnIndexOrThrow(MediaStore.Video.Media.DATE_ADDED)
                    while (c.moveToNext()) {
                        val id = c.getLong(iId)
                        list.add(
                            VideoItem(
                                id,
                                ContentUris.withAppendedId(MediaStore.Video.Media.EXTERNAL_CONTENT_URI, id),
                                c.getString(iName) ?: "video",
                                c.getLong(iDur),
                                c.getLong(iSize),
                                c.getString(iBucket) ?: "أخرى",
                                c.getLong(iDate)
                            )
                        )
                    }
                }
            } catch (e: Exception) {
                // ignore
            }
            runOnUiThread {
                all = list
                refresh()
            }
        }
    }

    private fun sorted(l: List<VideoItem>): List<VideoItem> = when (sortMode) {
        1 -> l.sortedBy { it.name.lowercase() }
        2 -> l.sortedByDescending { it.size }
        3 -> l.sortedByDescending { it.duration }
        else -> l.sortedByDescending { it.dateAdded }
    }

    private fun refresh() {
        val q = searchBox.text.toString().trim().lowercase()
        var list = all
        if (q.isNotEmpty()) list = list.filter { it.name.lowercase().contains(q) }
        val rows = ArrayList<Row>()
        if (showFolders && currentFolder == null && q.isEmpty()) {
            list.groupBy { it.folder }
                .toSortedMap(compareBy { it.lowercase() })
                .forEach { (k, v) -> rows.add(Row.Folder(k, v.size, v.sumOf { it.duration })) }
        } else {
            val f = currentFolder
            if (f != null) list = list.filter { it.folder == f }
            sorted(list).forEach { rows.add(Row.Vid(it)) }
        }
        titleView.text = currentFolder ?: "Night Player"
        rowAdapter.rows = rows
        rowAdapter.notifyDataSetChanged()
        if (rows.isEmpty()) {
            if (hasPerm()) showEmpty("لا توجد فيديوهات") else showEmpty("نحتاج إذن الوصول للفيديوهات.\nاضغط هنا لإعطاء الإذن")
        } else {
            emptyView.visibility = View.GONE
        }
    }

    private fun openPlayer(v: VideoItem) {
        val vids = rowAdapter.rows.filterIsInstance<Row.Vid>().map { it.v }
        val i = vids.indexOfFirst { it.id == v.id }.coerceAtLeast(0)
        startActivity(
            Intent(this, PlayerActivity::class.java)
                .putStringArrayListExtra("uris", ArrayList(vids.map { it.uri.toString() }))
                .putStringArrayListExtra("titles", ArrayList(vids.map { it.name }))
                .putExtra("index", i)
        )
    }

    private fun videoMenu(v: VideoItem) {
        val items = arrayOf("▶ تشغيل", "📤 مشاركة", "ℹ تفاصيل")
        AlertDialog.Builder(this)
            .setTitle(v.name)
            .setItems(items) { _, i ->
                when (i) {
                    0 -> openPlayer(v)
                    1 -> {
                        val s = Intent(Intent.ACTION_SEND)
                            .setType("video/*")
                            .putExtra(Intent.EXTRA_STREAM, v.uri)
                            .addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                        startActivity(Intent.createChooser(s, "مشاركة"))
                    }
                    else -> AlertDialog.Builder(this)
                        .setTitle("تفاصيل")
                        .setMessage(
                            "الاسم: ${v.name}\nالمجلد: ${v.folder}\nالحجم: ${formatSize(v.size)}\nالمدة: ${formatTime(v.duration)}"
                        )
                        .setPositiveButton("حسناً", null)
                        .show()
                }
            }.show()
    }

    private fun thumbFor(v: VideoItem): Bitmap? {
        return try {
            if (Build.VERSION.SDK_INT >= 29) {
                contentResolver.loadThumbnail(v.uri, Size(320, 180), null)
            } else {
                val r = MediaMetadataRetriever()
                try {
                    r.setDataSource(this, v.uri)
                    r.getFrameAtTime(1_000_000)
                } finally {
                    r.release()
                }
            }
        } catch (e: Exception) {
            null
        }
    }

    private fun loadThumb(v: VideoItem, iv: ImageView) {
        iv.tag = v.id
        val cached = thumbCache.get(v.id)
        if (cached != null) {
            iv.setImageBitmap(cached)
            return
        }
        iv.setImageDrawable(null)
        pool.execute {
            val bmp = thumbFor(v)
            if (bmp != null) {
                thumbCache.put(v.id, bmp)
                runOnUiThread {
                    if (iv.tag == v.id) iv.setImageBitmap(bmp)
                }
            }
        }
    }

    inner class RowAdapter : RecyclerView.Adapter<RowVH>() {
        var rows: List<Row> = emptyList()

        override fun getItemCount() = rows.size

        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RowVH {
            val ctx = this@MainActivity
            val card = LinearLayout(ctx).apply {
                orientation = LinearLayout.HORIZONTAL
                gravity = Gravity.CENTER_VERTICAL
                setPadding(dp(8), dp(8), dp(12), dp(8))
                background = roundBg(Night.CARD, 14)
                layoutParams = RecyclerView.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT
                ).apply { setMargins(dp(12), dp(5), dp(12), dp(5)) }
            }
            val box = FrameLayout(ctx).apply {
                background = roundBg(Night.CARD2, 10)
                clipToOutline = true
            }
            val img = ImageView(ctx).apply { scaleType = ImageView.ScaleType.CENTER_CROP }
            val icon = TextView(ctx).apply {
                text = "📁"
                textSize = 30f
                gravity = Gravity.CENTER
                visibility = View.GONE
            }
            val badge = TextView(ctx).apply {
                textSize = 11f
                setTextColor(Night.TEXT)
                background = roundBg(0xB3000000.toInt(), 6)
                setPadding(dp(5), dp(1), dp(5), dp(1))
            }
            box.addView(img, FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT))
            box.addView(icon, FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT))
            box.addView(
                badge,
                FrameLayout.LayoutParams(
                    ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT,
                    Gravity.BOTTOM or Gravity.END
                ).apply { setMargins(dp(4), dp(4), dp(4), dp(4)) }
            )
            card.addView(box, LinearLayout.LayoutParams(dp(124), dp(70)))

            val col = LinearLayout(ctx).apply { orientation = LinearLayout.VERTICAL }
            val title = TextView(ctx).apply {
                textSize = 15f
                maxLines = 2
                ellipsize = android.text.TextUtils.TruncateAt.END
                setTextColor(Night.TEXT)
            }
            val meta = TextView(ctx).apply {
                textSize = 12f
                setTextColor(Night.MUTED)
                setPadding(0, dp(4), 0, 0)
            }
            col.addView(title)
            col.addView(meta)
            val cp = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
            cp.marginStart = dp(12)
            card.addView(col, cp)
            return RowVH(card, img, icon, badge, title, meta)
        }

        override fun onBindViewHolder(h: RowVH, position: Int) {
            when (val row = rows[position]) {
                is Row.Folder -> {
                    h.img.setImageDrawable(null)
                    h.img.tag = -1L
                    h.icon.visibility = View.VISIBLE
                    h.badge.visibility = View.GONE
                    h.title.text = row.name
                    h.meta.text = "${row.count} فيديو · ${formatTime(row.total)}"
                    h.card.setOnClickListener {
                        currentFolder = row.name
                        refresh()
                    }
                    h.card.setOnLongClickListener(null)
                }
                is Row.Vid -> {
                    val v = row.v
                    h.icon.visibility = View.GONE
                    h.badge.visibility = View.VISIBLE
                    h.badge.text = formatTime(v.duration)
                    h.title.text = v.name
                    val saved = prefs.getLong("pos_" + v.uri.toString(), 0L)
                    var m = "${formatSize(v.size)} · ${v.folder}"
                    if (saved > 5000) m += "  ▶ ${formatTime(saved)}"
                    h.meta.text = m
                    loadThumb(v, h.img)
                    h.card.setOnClickListener { openPlayer(v) }
                    h.card.setOnLongClickListener {
                        videoMenu(v)
                        true
                    }
                }
            }
        }
    }
}
=== app/src/main/java/com/nightplayer/app/PlayerActivity.kt ===
@file:OptIn(androidx.media3.common.util.UnstableApi::class)

package com.nightplayer.app

import android.app.AlertDialog
import android.app.PictureInPictureParams
import android.content.ComponentName
import android.content.Intent
import android.content.pm.ActivityInfo
import android.content.res.Configuration
import android.graphics.Color
import android.graphics.drawable.GradientDrawable
import android.media.AudioManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Rational
import android.view.Gravity
import android.view.GestureDetector
import android.view.MotionEvent
import android.view.ScaleGestureDetector
import android.view.View
import android.view.ViewGroup
import android.view.WindowManager
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import androidx.media3.common.C
import androidx.media3.common.MediaItem
import androidx.media3.common.MediaMetadata
import androidx.media3.common.MimeTypes
import androidx.media3.common.PlaybackException
import androidx.media3.common.Player
import androidx.media3.common.VideoSize
import androidx.media3.common.util.RepeatModeUtil
import androidx.media3.session.MediaController
import androidx.media3.session.SessionToken
import androidx.media3.ui.AspectRatioFrameLayout
import androidx.media3.ui.CaptionStyleCompat
import androidx.media3.ui.PlayerView
import com.google.common.util.concurrent.ListenableFuture
import kotlin.math.abs
import kotlin.math.roundToInt

class PlayerActivity : ComponentActivity() {

    private lateinit var root: FrameLayout
    private lateinit var playerView: PlayerView
    private lateinit var topBar: LinearLayout
    private lateinit var titleView: TextView
    private lateinit var infoText: TextView
    private lateinit var unlockBtn: TextView

    private var controller: MediaController? = null
    private var future: ListenableFuture<MediaController>? = null
    private val handler = Handler(Looper.getMainLooper())
    private val prefs by lazy { getSharedPreferences("night", MODE_PRIVATE) }

    private var uris = ArrayList<String>()
    private var titles = ArrayList<String>()
    private var startIndex = 0

    private var locked = false
    private var inPip = false
    private var bgPlay = false
    private var resizeIdx = 0
    private var orientIdx = 0
    private var zoom = 1f
    private var sleepRunnable: Runnable? = null

    private var gMode = 0
    private var startVol = 0
    private var startBright = 0.5f
    private var startPos = 0L
    private var seekTarget = -1L

    private val resizeModes = intArrayOf(
        AspectRatioFrameLayout.RESIZE_MODE_FIT,
        AspectRatioFrameLayout.RESIZE_MODE_FILL,
        AspectRatioFrameLayout.RESIZE_MODE_ZOOM,
        AspectRatioFrameLayout.RESIZE_MODE_FIXED_WIDTH,
        AspectRatioFrameLayout.RESIZE_MODE_FIXED_HEIGHT
    )
    private val resizeNames = arrayOf("ملائم", "تمديد لملء الشاشة", "قص وتكبير", "عرض ثابت", "ارتفاع ثابت")

    private val hideInfo = Runnable { infoText.visibility = View.GONE }
    private val hideUnlock = Runnable { unlockBtn.visibility = View.GONE }

    private val subPicker =
        registerForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
            if (uri != null) addSubtitle(uri)
        }

    private val listener = object : Player.Listener {
        override fun onMediaItemTransition(mediaItem: MediaItem?, reason: Int) {
            zoom = 1f
            applyZoom()
            updateTitle()
        }

        override fun onMediaMetadataChanged(mediaMetadata: MediaMetadata) {
            updateTitle()
        }

        override fun onPlayerError(error: PlaybackException) {
            Toast.makeText(
                this@PlayerActivity,
                "تعذر تشغيل الفيديو: " + error.errorCodeName,
                Toast.LENGTH_LONG
            ).show()
        }

        override fun onIsPlayingChanged(isPlaying: Boolean) {
            if (!isPlaying) saveProgress()
        }

        override fun onVideoSizeChanged(videoSize: VideoSize) {
            updatePipParams()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        if (Build.VERSION.SDK_INT >= 28) {
            val lp = window.attributes
            lp.layoutInDisplayCutoutMode =
                WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES
            window.attributes = lp
        }
        parseIntent(intent)
        buildUi()
        setupGestures()
        hideSystemUi()
        connect()
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        setIntent(intent)
        parseIntent(intent)
        startQueue()
    }

    private fun parseIntent(i: Intent) {
        val u = i.getStringArrayListExtra("uris")
        val d = i.data
        if (u != null) {
            uris = u
            titles = i.getStringArrayListExtra("titles") ?: ArrayList(u)
            startIndex = i.getIntExtra("index", 0)
        } else if (d != null) {
            uris = arrayListOf(d.toString())
            titles = arrayListOf(d.lastPathSegment ?: "Video")
            startIndex = 0
        } else {
            uris = ArrayList()
            titles = ArrayList()
        }
    }

    // ---------------------------------------------------------------- UI

    private fun buildUi() {
        root = FrameLayout(this).apply { setBackgroundColor(Color.BLACK) }

        playerView = PlayerView(this).apply {
            useController = true
            controllerShowTimeoutMs = 3500
            setShowSubtitleButton(true)
            setShowShuffleButton(true)
            setRepeatToggleModes(
                RepeatModeUtil.REPEAT_TOGGLE_MODE_ONE or RepeatModeUtil.REPEAT_TOGGLE_MODE_ALL
            )
            resizeMode = AspectRatioFrameLayout.RESIZE_MODE_FIT
            subtitleView?.setStyle(
                CaptionStyleCompat(
                    Color.WHITE, Color.TRANSPARENT, Color.TRANSPARENT,
                    CaptionStyleCompat.EDGE_TYPE_OUTLINE, Color.BLACK, null
                )
            )
            setControllerVisibilityListener(PlayerView.ControllerVisibilityListener { v ->
                if (::topBar.isInitialized) {
                    topBar.visibility =
                        if (v == View.VISIBLE && !locked && !inPip) View.VISIBLE else View.GONE
                }
            })
        }
        root.addView(
            playerView,
            FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)
        )

        topBar = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(dp(8), dp(8), dp(8), dp(24))
            background = GradientDrawable(
                GradientDrawable.Orientation.TOP_BOTTOM,
                intArrayOf(0xCC000000.toInt(), 0x00000000)
            )
            visibility = View.GONE
        }
        topBar.addView(iconButton("←", 22) { finish() })
        titleView = TextView(this).apply {
            textSize = 15f
            setTextColor(Color.WHITE)
            isSingleLine = true
            ellipsize = android.text.TextUtils.TruncateAt.MARQUEE
            marqueeRepeatLimit = -1
            isSelected = true
        }
        topBar.addView(titleView, LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f))
        topBar.addView(iconButton("⤢") { cycleResize() })
        topBar.addView(iconButton("🔒") { lockScreen() })
        topBar.addView(iconButton("▣") { enterPip() })
        topBar.addView(iconButton("⋮", 22) { showMore() })
        root.addView(
            topBar,
            FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.TOP
            )
        )

        infoText = TextView(this).apply {
            textSize = 20f
            setTextColor(Color.WHITE)
            gravity = Gravity.CENTER
            background = roundBg(0xB3121829.toInt(), 14)
            setPadding(dp(20), dp(12), dp(20), dp(12))
            visibility = View.GONE
        }
        root.addView(
            infoText,
            FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.CENTER
            )
        )

        unlockBtn = TextView(this).apply {
            text = "🔓  اضغط لفتح القفل"
            textSize = 16f
            setTextColor(Color.WHITE)
            background = roundBg(Night.ACCENT, 24)
            setPadding(dp(20), dp(12), dp(20), dp(12))
            visibility = View.GONE
            setOnClickListener { unlockScreen() }
        }
        root.addView(
            unlockBtn,
            FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.CENTER
            )
        )

        ViewCompat.setOnApplyWindowInsetsListener(root) { _, insets ->
            val i = insets.getInsets(
                WindowInsetsCompat.Type.displayCutout() or WindowInsetsCompat.Type.systemBars()
            )
            topBar.setPadding(dp(8) + i.left, dp(8) + i.top, dp(8) + i.right, dp(24))
            insets
        }
        setContentView(root)
    }

    private fun hideSystemUi() {
        WindowCompat.setDecorFitsSystemWindows(window, false)
        val ic = WindowInsetsControllerCompat(window, window.decorView)
        ic.hide(WindowInsetsCompat.Type.systemBars())
        ic.systemBarsBehavior = WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
    }

    override fun onWindowFocusChanged(hasFocus: Boolean) {
        super.onWindowFocusChanged(hasFocus)
        if (hasFocus) hideSystemUi()
    }

    private fun showInfo(t: String) {
        infoText.text = t
        infoText.visibility = View.VISIBLE
        handler.removeCallbacks(hideInfo)
        handler.postDelayed(hideInfo, 900)
    }

    private fun showUnlock() {
        unlockBtn.visibility = View.VISIBLE
        handler.removeCallbacks(hideUnlock)
        handler.postDelayed(hideUnlock, 2500)
    }

    private fun updateTitle() {
        val c = controller
        val t: CharSequence = c?.mediaMetadata?.title
            ?: titles.getOrNull(startIndex)
            ?: ""
        titleView.text = t
    }

    // ---------------------------------------------------------------- gestures

    private fun currentBrightness(): Float {
        val b = window.attributes.screenBrightness
        return if (b >= 0f) b else 0.5f
    }

    private fun setBrightness(b: Float) {
        val lp = window.attributes
        lp.screenBrightness = b
        window.attributes = lp
    }

    private fun applyZoom() {
        playerView.videoSurfaceView?.let {
            it.scaleX = zoom
            it.scaleY = zoom
        }
    }

    private fun seekBy(ms: Long) {
        val c = controller ?: return
        val d = c.duration
        val target = if (d > 0) (c.currentPosition + ms).coerceIn(0L, d)
        else (c.currentPosition + ms).coerceAtLeast(0L)
        c.seekTo(target)
        showInfo(if (ms >= 0) "⏩ +" + (ms / 1000) + "s" else "⏪ -" + (-ms / 1000) + "s")
    }

    private fun endGesture() {
        val c = controller
        if (gMode == 1 && seekTarget >= 0 && c != null) {
            c.seekTo(seekTarget)
        }
        seekTarget = -1L
        gMode = 0
    }

    private fun setupGestures() {
        val am = getSystemService(AUDIO_SERVICE) as AudioManager
        val maxVol = am.getStreamMaxVolume(AudioManager.STREAM_MUSIC)

        val gd = GestureDetector(this, object : GestureDetector.SimpleOnGestureListener() {
            override fun onDown(e: MotionEvent): Boolean {
                gMode = 0
                startVol = am.getStreamVolume(AudioManager.STREAM_MUSIC)
                startBright = currentBrightness()
                startPos = controller?.currentPosition ?: 0L
                return true
            }

            override fun onDoubleTap(e: MotionEvent): Boolean {
                val c = controller ?: return false
                val w = playerView.width.toFloat()
                if (e.x < w / 3f) seekBy(-10000L)
                else if (e.x > w * 2f / 3f) seekBy(10000L)
                else if (c.isPlaying) c.pause() else c.play()
                return true
            }

            override fun onScroll(e1: MotionEvent?, e2: MotionEvent, dx: Float, dy: Float): Boolean {
                if (e1 == null) return false
                val dX = e2.x - e1.x
                val dY = e2.y - e1.y
                if (gMode == 0) {
                    gMode = if (abs(dX) > abs(dY)) 1
                    else if (e1.x < playerView.width / 2f) 2
                    else 3
                }
                val h = playerView.height.toFloat()
                when (gMode) {
                    1 -> {
                        val c = controller ?: return true
                        val dur = c.duration
                        if (dur <= 0) return true
                        val delta = (dX / playerView.width * 120000f).toLong()
                        val target = (startPos + delta).coerceIn(0L, dur)
                        seekTarget = target
                        val sign = if (delta >= 0) "+" else "-"
                        showInfo(formatTime(target) + "  (" + sign + formatTime(abs(delta)) + ")")
                    }
                    2 -> {
                        val b = (startBright - dY / h * 1.2f).coerceIn(0.02f, 1f)
                        setBrightness(b)
                        showInfo("☀ " + (b * 100).toInt() + "%")
                    }
                    3 -> {
                        val nv = (startVol + (-dY / h * maxVol * 1.3f)).roundToInt().coerceIn(0, maxVol)
                        am.setStreamVolume(AudioManager.STREAM_MUSIC, nv, 0)
                        showInfo("🔊 " + (nv * 100 / maxVol) + "%")
                    }
                }
                return true
            }
        })

        val sd = ScaleGestureDetector(this, object : ScaleGestureDetector.SimpleOnScaleGestureListener() {
            override fun onScale(detector: ScaleGestureDetector): Boolean {
                zoom = (zoom * detector.scaleFactor).coerceIn(1f, 4f)
                applyZoom()
                showInfo("🔍 " + (zoom * 100).toInt() + "%")
                return true
            }
        })

        playerView.setOnTouchListener { _, e ->
            if (locked) {
                if (e.actionMasked == MotionEvent.ACTION_UP) showUnlock()
                true
            } else {
                sd.onTouchEvent(e)
                if (!sd.isInProgress) gd.onTouchEvent(e)
                if (e.actionMasked == MotionEvent.ACTION_UP || e.actionMasked == MotionEvent.ACTION_CANCEL) {
                    endGesture()
                }
                false
            }
        }
    }

    // ---------------------------------------------------------------- controller

    private fun connect() {
        val token = SessionToken(this, ComponentName(this, PlaybackService::class.java))
        val f = MediaController.Builder(this, token).buildAsync()
        future = f
        f.addListener({
            try {
                controller = f.get()
                onConnected()
            } catch (e: Exception) {
                Toast.makeText(this, "تعذر تشغيل خدمة المشغل", Toast.LENGTH_LONG).show()
                finish()
            }
        }, ContextCompat.getMainExecutor(this))
    }

    private fun onConnected() {
        val c = controller ?: return
        playerView.player = c
        c.addListener(listener)
        startQueue()
    }

    private fun startQueue() {
        val c = controller ?: return
        if (uris.isEmpty()) {
            if (c.mediaItemCount == 0) finish()
            updateTitle()
            return
        }
        val same = c.mediaItemCount == uris.size &&
            uris.indices.all { c.getMediaItemAt(it).mediaId == uris[it] }
        if (same) {
            if (c.currentMediaItemIndex != startIndex) c.seekToDefaultPosition(startIndex)
            if (!c.isPlaying) c.play()
        } else {
            val items = uris.mapIndexed { i, u ->
                MediaItem.Builder()
                    .setMediaId(u)
                    .setUri(u)
                    .setMediaMetadata(
                        MediaMetadata.Builder().setTitle(titles.getOrElse(i) { u }).build()
                    )
                    .build()
            }
            val idx = startIndex.coerceIn(0, items.size - 1)
            val resume = prefs.getLong("pos_" + uris[idx], 0L)
            c.setMediaItems(items, idx, if (resume > 5000) resume else 0L)
            c.prepare()
            c.play()
        }
        updateTitle()
    }

    private fun saveProgress() {
        val c = controller ?: return
        val item = c.currentMediaItem ?: return
        val d = c.duration
        val p = c.currentPosition
        val key = "pos_" + item.mediaId
        if (d > 0 && p > 5000 && p < d - 10000) {
            prefs.edit().putLong(key, p).apply()
        } else {
            prefs.edit().remove(key).apply()
        }
    }

    // ---------------------------------------------------------------- actions

    private fun cycleResize() {
        resizeIdx = (resizeIdx + 1) % resizeModes.size
        playerView.resizeMode = resizeModes[resizeIdx]
        showInfo(resizeNames[resizeIdx])
    }

    private fun lockScreen() {
        locked = true
        playerView.useController = false
        topBar.visibility = View.GONE
        showInfo("🔒 تم قفل الشاشة")
        showUnlock()
    }

    private fun unlockScreen() {
        locked = false
        playerView.useController = true
        unlockBtn.visibility = View.GONE
        playerView.showController()
        showInfo("🔓 تم فتح القفل")
    }

    private fun updatePipParams() {
        if (Build.VERSION.SDK_INT < 26) return
        val vs = controller?.videoSize ?: return
        if (vs.width <= 0 || vs.height <= 0) return
        try {
            setPictureInPictureParams(buildPipParams(vs))
        } catch (e: Exception) {
            // ignore
        }
    }

    private fun buildPipParams(vs: VideoSize?): PictureInPictureParams {
        var r = 16f / 9f
        if (vs != null && vs.width > 0 && vs.height > 0) {
            r = vs.width.toFloat() / vs.height.toFloat()
        }
        r = r.coerceIn(0.45f, 2.3f)
        return PictureInPictureParams.Builder()
            .setAspectRatio(Rational((r * 1000).toInt(), 1000))
            .build()
    }

    private fun enterPip() {
        if (Build.VERSION.SDK_INT < 26) {
            Toast.makeText(this, "غير مدعوم في هذا الإصدار", Toast.LENGTH_SHORT).show()
            return
        }
        try {
            enterPictureInPictureMode(buildPipParams(controller?.videoSize))
        } catch (e: Exception) {
            Toast.makeText(this, "الصورة داخل الصورة غير متاحة", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onUserLeaveHint() {
        super.onUserLeaveHint()
        if (!locked && !bgPlay && controller?.isPlaying == true) enterPip()
    }

    override fun onPictureInPictureModeChanged(
        isInPictureInPictureMode: Boolean,
        newConfig: Configuration
    ) {
        super.onPictureInPictureModeChanged(isInPictureInPictureMode, newConfig)
        inPip = isInPictureInPictureMode
        playerView.useController = !isInPictureInPictureMode && !locked
        if (isInPictureInPictureMode) topBar.visibility = View.GONE
    }

    private fun showMore() {
        val items = arrayOf(
            "📝 تحميل ترجمة خارجية (SRT / VTT / ASS)",
            "⏲ مؤقت النوم",
            "🔄 تدوير الشاشة",
            if (bgPlay) "🎧 التشغيل في الخلفية: مفعّل" else "🎧 التشغيل في الخلفية: متوقف",
            "🔠 حجم الترجمة",
            "⏭ تخطي 85 ثانية",
            "ℹ معلومات الفيديو"
        )
        AlertDialog.Builder(this)
            .setItems(items) { _, i ->
                when (i) {
                    0 -> subPicker.launch(arrayOf("*/*"))
                    1 -> sleepDialog()
                    2 -> rotate()
                    3 -> {
                        bgPlay = !bgPlay
                        Toast.makeText(
                            this,
                            if (bgPlay) "سيستمر الصوت عند الخروج من التطبيق" else "سيتوقف التشغيل عند الخروج",
                            Toast.LENGTH_SHORT
                        ).show()
                    }
                    4 -> subtitleSizeDialog()
                    5 -> seekBy(85000L)
                    else -> infoDialog()
                }
            }.show()
    }

    private fun rotate() {
        orientIdx = (orientIdx + 1) % 3
        requestedOrientation = when (orientIdx) {
            0 -> ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
            1 -> ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
            else -> ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
        }
        showInfo(arrayOf("تدوير تلقائي", "أفقي", "عمودي")[orientIdx])
    }

    private fun sleepDialog() {
        val opts = arrayOf("إيقاف المؤقت", "15 دقيقة", "30 دقيقة", "45 دقيقة", "60 دقيقة", "90 دقيقة")
        val mins = intArrayOf(0, 15, 30, 45, 60, 90)
        AlertDialog.Builder(this)
            .setTitle("مؤقت النوم")
            .setItems(opts) { _, i ->
                sleepRunnable?.let { handler.removeCallbacks(it) }
                sleepRunnable = null
                if (mins[i] > 0) {
                    val r = Runnable {
                        controller?.pause()
                        Toast.makeText(this, "أوقفه مؤقت النوم", Toast.LENGTH_LONG).show()
                    }
                    sleepRunnable = r
                    handler.postDelayed(r, mins[i] * 60000L)
                    Toast.makeText(this, "سيتوقف الفيديو بعد " + opts[i], Toast.LENGTH_SHORT).show()
                } else {
                    Toast.makeText(this, "تم إلغاء المؤقت", Toast.LENGTH_SHORT).show()
                }
            }.show()
    }

    private fun subtitleSizeDialog() {
        val opts = arrayOf("صغير", "عادي", "كبير", "كبير جداً")
        val sizes = floatArrayOf(0.04f, 0.0533f, 0.07f, 0.09f)
        AlertDialog.Builder(this)
            .setTitle("حجم الترجمة")
            .setItems(opts) { _, i ->
                playerView.subtitleView?.setFractionalTextSize(sizes[i])
            }.show()
    }

    private fun addSubtitle(uri: Uri) {
        val c = controller ?: return
        val cur = c.currentMediaItem ?: return
        val name = (uri.lastPathSegment ?: "").lowercase()
        val mime = when {
            name.endsWith(".vtt") -> MimeTypes.TEXT_VTT
            name.endsWith(".ass") || name.endsWith(".ssa") -> MimeTypes.TEXT_SSA
            name.endsWith(".ttml") || name.endsWith(".xml") -> MimeTypes.APPLICATION_TTML
            else -> MimeTypes.APPLICATION_SUBRIP
        }
        val sub = MediaItem.SubtitleConfiguration.Builder(uri)
            .setMimeType(mime)
            .setLanguage("und")
            .setLabel("ترجمة خارجية")
            .setSelectionFlags(C.SELECTION_FLAG_DEFAULT)
            .build()
        val newItem = MediaItem.Builder()
            .setMediaId(cur.mediaId)
            .setUri(cur.mediaId)
            .setMediaMetadata(cur.mediaMetadata)
            .setSubtitleConfigurations(listOf(sub))
            .build()
        val idx = c.currentMediaItemIndex
        val pos = c.currentPosition
        c.replaceMediaItem(idx, newItem)
        c.seekTo(idx, pos)
        c.play()
        showInfo("📝 تم تحميل الترجمة")
    }

    private fun infoDialog() {
        val c = controller ?: return
        val vs = c.videoSize
        val sb = StringBuilder()
        sb.append("الدقة: ").append(vs.width).append("x").append(vs.height).append("\n")
        sb.append("المدة: ").append(formatTime(if (c.duration > 0) c.duration else 0L)).append("\n")
        for (g in c.currentTracks.groups) {
            for (i in 0 until g.length) {
                if (g.isTrackSelected(i)) {
                    val f = g.getTrackFormat(i)
                    val label = when (g.type) {
                        C.TRACK_TYPE_VIDEO -> "فيديو"
                        C.TRACK_TYPE_AUDIO -> "صوت"
                        C.TRACK_TYPE_TEXT -> "ترجمة"
                        else -> "أخرى"
                    }
                    sb.append(label).append(": ").append(f.sampleMimeType ?: "?")
                    if (f.codecs != null) sb.append(" (").append(f.codecs).append(")")
                    sb.append("\n")
                }
            }
        }
        AlertDialog.Builder(this)
            .setTitle("معلومات الفيديو")
            .setMessage(sb.toString())
            .setPositiveButton("حسناً", null)
            .show()
    }

    // ---------------------------------------------------------------- lifecycle

    override fun onStop() {
        super.onStop()
        saveProgress()
        if (!bgPlay) controller?.pause()
    }

    override fun onDestroy() {
        sleepRunnable?.let { handler.removeCallbacks(it) }
        handler.removeCallbacksAndMessages(null)
        controller?.removeListener(listener)
        if (isFinishing && !bgPlay) {
            controller?.stop()
        }
        playerView.player = null
        future?.let { MediaController.releaseFuture(it) }
        controller = null
        super.onDestroy()
    }
}
'''

parts = re.split(r'^=== (.+?) ===\n', BUNDLE, flags=re.M)
count = 0
for i in range(1, len(parts), 2):
    path = parts[i].strip()
    content = parts[i + 1]
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    count += 1
    print("created:", path)
print("Total files:", count)
