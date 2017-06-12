package in.peerreview.bengaligossip;

import android.graphics.drawable.Drawable;
import android.os.Build;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.text.Spannable;
import android.text.SpannableString;
import android.text.style.AbsoluteSizeSpan;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import com.squareup.okhttp.Callback;
import com.squareup.okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.Response;
import com.squareup.picasso.Picasso;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MainActivity extends AppCompatActivity {
    public static OkHttpClient client = new OkHttpClient();

    private static List<News> newsList = new ArrayList<>();
    private static int newsListIdx = -1;
    private static int page = 0;
    private Button fetchButton, nextButton, prevButton;
    private ScrollView hsv;
    private ImageView images;
    private TextView title, fullstory;
    private boolean fetch_in_progress = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        fetchButton = (Button) findViewById(R.id.fetchButton);
        nextButton = (Button) findViewById(R.id.nextButton);
        prevButton = (Button) findViewById(R.id.prevButton);

        images = (ImageView) findViewById(R.id.img);
        title = (TextView) findViewById(R.id.title);
        fullstory = (TextView) findViewById(R.id.fullstory);
        hsv =(ScrollView) findViewById(R.id.hsv);

        fetchButton.setOnClickListener(listener);
        nextButton.setOnClickListener(listener);
        prevButton.setOnClickListener(listener);
        add();
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
            Window w = getWindow(); // in Activity's onCreate() for instance
            w.setFlags(WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS, WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS);
        }
    }

    View.OnClickListener listener = new View.OnClickListener() {

        @Override
        public void onClick(View v) {
            switch (v.getId()) {
                case R.id.fetchButton:
                    try {
                        doGetRequest("http://52.89.112.230/api/banglagossip2?page=" + page + "&limit=10");
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                    break;

                case R.id.nextButton:
                    if(newsList.size() - newsListIdx < 5 ){
                        try {
                            doGetRequest("http://52.89.112.230/api/banglagossip2?page=" + page + "&limit=10");
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                    newsListIdx++;
                    renderData(newsListIdx);
                    break;

                case R.id.prevButton:
                    newsListIdx--;
                    renderData(newsListIdx);
                    break;

                default:
                    break;
            }

        }
    };

    void doGetRequest(String url) throws IOException {
        if(fetch_in_progress == true){
            Toast.makeText(MainActivity.this, "Fetching request ignored as one request in progress.", Toast.LENGTH_LONG).show();
            return ;
        }
        fetch_in_progress = true;
        Request request = new Request.Builder()
                .url(url)
                .build();

        client.newCall(request)
                .enqueue(new Callback() {

                    @Override
                    public void onFailure(Request request, IOException e) {
                        fetch_in_progress = false;
                        // Error
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                Toast.makeText(MainActivity.this, "Fetching request Failed.", Toast.LENGTH_LONG).show();
                            }
                        });
                    }

                    @Override
                    public void onResponse(Response response) throws IOException {
                        fetch_in_progress = false;
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                Toast.makeText(MainActivity.this, "Fetching request succeed.", Toast.LENGTH_LONG).show();
                            }
                        });
                        String jsonData = response.body().string();
                        JSONObject Jobject = null;
                        try {
                            Jobject = new JSONObject(jsonData);
                            JSONArray Jarray = Jobject.getJSONArray("out");

                            for (int i = 0; i < Jarray.length(); i++) {
                                JSONObject object = Jarray.getJSONObject(i);
                                newsList.add(new News(object.getString("title"), object.getString("fullstory"), object.getString("main_img"), null, null));
                            }
                            if (Jarray.length() != 0) {
                                runOnUiThread(new Runnable() {
                                    @Override
                                    public void run() {
/*
                                        newsListIdx++;
                                        renderData(newsListIdx);
                                        page++;
*/
                                    }
                                });
                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                });
    }

    public void renderData(int idx) {
        if (idx < 0) {
            Toast.makeText(this, "You at the begging so can't call previous", Toast.LENGTH_LONG).show();
            return;
        }
        if (idx >= newsList.size()) {
            Toast.makeText(this, "Fetching the news from server ..wait..", Toast.LENGTH_LONG).show();
            return;
        }
        News now = newsList.get(idx);
        title.setText(now.getTitle());

        String text = now.getFullstory();
        String formattedText = text.replaceAll("\n", "\n\n");
        SpannableString spannableString = new SpannableString(formattedText);

        Matcher matcher = Pattern.compile("\n\n").matcher(formattedText);
        while (matcher.find()) {
            spannableString.setSpan(new AbsoluteSizeSpan(20, true), matcher.start() + 1, matcher.end(), Spannable.SPAN_EXCLUSIVE_EXCLUSIVE);
        }

        fullstory.setText(spannableString);
        try {
            Picasso.with(this).load(now.getImgurl()).into(images);
        }
        catch (Exception e) {
            int imageResource = getResources().getIdentifier("@drawable/noimg", null, getPackageName());
            Drawable res = getResources().getDrawable(imageResource);
            images.setImageDrawable(res);
            e.printStackTrace();
        }
        hsv.fullScroll(View.FOCUS_UP);
    }

    class News {
        public News(String title, String fullstory, String imgurl, String sources, String type) {
            this.title = title;
            this.fullstory = fullstory;
            this.imgurl = imgurl;
            this.sources = sources;
            this.type = type;
        }

        public String getTitle() {
            return title;
        }

        public void setTitle(String title) {
            this.title = title;
        }

        public String getFullstory() {
            return fullstory;
        }

        public void setFullstory(String fullstory) {
            this.fullstory = fullstory;
        }

        public String getImgurl() {
            return imgurl;
        }

        public void setImgurl(String imgurl) {
            this.imgurl = imgurl;
        }

        public String getSources() {
            return sources;
        }

        public void setSources(String sources) {
            this.sources = sources;
        }

        public String getType() {
            return type;
        }

        public void setType(String type) {
            this.type = type;
        }

        private String title;
        private String fullstory;
        private String imgurl;
        private String sources;
        private String type;
    }

    public void add() {
        newsList.add(new News(
                "আলু, শশা, টোম্যাটো বেশি খেলে কিন্তু বিপদ হতে পারে",
                "আলু, শশা, টোম্যাটো তিনটেই অত্যন্ত পুষ্টিকর খাবার। প্রতি দিনের প্রয়োজনীয় কার্বোহাইড্রেট, ভিটামিনের যেমন অন্যতম উত্স আলু, তেমনই প্রচুর ভিটামিন এবং অ্যান্টিঅক্সিড্যান্টে ভরপুর শশা, টোম্যাটো। বিশেষ করে গরমকালে বেশি করে স্যালাড খাওয়ার পরামর্শ দিয়ে থাকেন বিশেষজ্ঞরা। তবে খুব বেশি এগুলো খাওয়াও কিন্তু ঘটাতে পারে হিতে বিপরীত ফল। নতুন এক গবেষণার ফল বলছে- আলু, শশা, টোম্যাটোর মধ্যে থাকে এমন এক প্রোটিন যা বাড়িয়ে দেয় অ্যালঝাইমার’স-এর ঝুঁকি।\n" +
                        "ক্যালিফোর্নিয়ার কার্ডিওলজিস্ট ও হার্ট সার্জন স্টিভেন গন্ড্রি জানাচ্ছেন- শশা, টোম্যাটো, গোটা শস্য, সয়, ক্যাপসিকাম, আলু, কল বেরনো ছোলা ও ডেয়ারি প্রডাক্টে থাকা লেকটিন নামক প্রোটিন আমাদের স্মৃতিশক্তি নষ্ট করে দিতে পারে। একই মত ইংল্যান্ডের চিকিত্সক টম গ্রিনফিল্ডেরও। রক্তের বিভিন্ন গ্রুপের উপর তিনি লেকটিনের প্রভাব পরীক্ষা করেন। ফলাফলে জানিয়েছেন, শরীর লেকটিনের পরিমাণ অতিরিক্ত হয়ে গেলে তা ব্রেন ডিজঅর্ডারেরও কারণ হয়ে উঠতে পারে।\n" +
                        "গ্রিনফিল্ড জানান, এই লেকটিন ঠিক কতটা প্রভাব ফেলবে, মস্তিষ্ক কতটা ক্ষতিগ্রস্ত হবে তা নির্ভর করে জিনের উপর। রক্তের গ্রুপ অনুযায়ী লেকটিনের প্রভাবও বদলে যায়। রক্তের ইনসুলিন রিসেপটর ব্লক করে রক্তনালীর উপর প্রভাব ফেলতে পারে, মস্তিষ্কও ক্ষতিগ্রস্ত হয়। তবে লেকটিন ডায়েট থেকে সম্পূর্ণ বাদ দেওয়া সম্ভব নয়। প্রথমত, এই সব খাবার অত্যন্ত পুষ্টিকর, এবং দ্বিতীয়ত, জিনের গঠন অনুযায়ী এর মধ্যে কোনও খাবার কারও জন্য ভাল, সেই খাবারই আবার অন্যের জন্য ভিলেন হয়ে উঠতে পারে।"
                , "http://images1.anandabazar.com/polopoly_fs/1.616659.1495449369!/image/image.jpg_gen/derivatives/landscape_390/image.jpg",
                null, null
        ));
    }
}
