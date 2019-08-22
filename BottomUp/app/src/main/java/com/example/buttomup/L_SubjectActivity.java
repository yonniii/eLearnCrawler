package com.example.buttomup;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.widget.EditText;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;

public class L_SubjectActivity extends AppCompatActivity {
    private RecyclerView recyclerView;
    private ArrayList<L_SubjectData> arrayList;
    private LSubjectAdapter subjectAdapter;
    private String mJsonString;
    String stdnt;
    ArrayList<String> subject = new ArrayList<String>();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_l__subject);
        Intent intent = getIntent();
        stdnt = intent.getStringExtra("data");
        recyclerView = (RecyclerView) findViewById(R.id.lecture_subject);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));

        arrayList = new ArrayList<>();

        arrayList.clear();
        subjectAdapter = new LSubjectAdapter(this, arrayList);
        recyclerView.setAdapter(subjectAdapter);

        arrayList.clear();
        subjectAdapter.notifyDataSetChanged();

        L_SubjectActivity.GetData task = new L_SubjectActivity.GetData();
        task.execute("http://ec2-54-180-87-74.ap-northeast-2.compute.amazonaws.com/lectures.php","");
    }

    private class GetData extends AsyncTask<String, Void, String> {
        ProgressDialog progressDialog;
        String errorString = null;

        @Override
        protected  void onPreExecute(){
            super.onPreExecute();

            progressDialog = ProgressDialog.show(L_SubjectActivity.this,"Please Wait", null, true, true);
        }

        @Override
        protected  void onPostExecute(String result){
            super.onPostExecute(result);

            progressDialog.dismiss();
            mJsonString = result;
            showResult();
        }

        @Override
        protected String doInBackground(String... params){
            String serverURL = params[0];
            String postParameters = params[1];

            try {

                URL url = new URL(serverURL);
                HttpURLConnection httpURLConnection = (HttpURLConnection) url.openConnection();


                httpURLConnection.setReadTimeout(5000);
                httpURLConnection.setConnectTimeout(5000);
                httpURLConnection.setRequestMethod("POST");
                httpURLConnection.setDoInput(true);
                httpURLConnection.connect();


                OutputStream outputStream = httpURLConnection.getOutputStream();
                outputStream.write(postParameters.getBytes("UTF-8"));
                outputStream.flush();
                outputStream.close();


                int responseStatusCode = httpURLConnection.getResponseCode();

                InputStream inputStream;
                if(responseStatusCode == HttpURLConnection.HTTP_OK) {
                    inputStream = httpURLConnection.getInputStream();
                }
                else{
                    inputStream = httpURLConnection.getErrorStream();
                }


                InputStreamReader inputStreamReader = new InputStreamReader(inputStream, "UTF-8");
                BufferedReader bufferedReader = new BufferedReader(inputStreamReader);

                StringBuilder sb = new StringBuilder();
                String line;

                while((line = bufferedReader.readLine()) != null){
                    sb.append(line);
                }

                bufferedReader.close();

                return sb.toString().trim();


            } catch (Exception e) {
                errorString = e.toString();
                return null;
            }

        }
    }

    private void showResult(){
        String TAG_STDNT_NO = "stdnt_no";
        String TAG_ID = "id";
        String TAG_JSON="lectures";
        String TAG_TITLE = "title";
        String TAG_START = "start_time";
        String TAG_END = "end_time";
        String TAG_SUBJECT = "subject";
        String TAG_STATE = "state";
        try{
            JSONObject jsonObject = new JSONObject(mJsonString);
            System.out.println("mJSonString : "+mJsonString);
            JSONArray jsonArray = jsonObject.getJSONArray(TAG_JSON);

            for(int i = 0;i<jsonArray.length();i++){
                JSONObject item = jsonArray.getJSONObject(i);
                String stdnt_no = item.getString(TAG_STDNT_NO);
                String Id = item.getString(TAG_ID);
                String title = item.getString(TAG_TITLE);
                String start = item.getString(TAG_START);
                String end = item.getString(TAG_END);
                String temp = item.getString(TAG_SUBJECT);
                String state = item.getString(TAG_STATE);
                if((stdnt.equals(stdnt_no))&&(!subject.contains(temp))) {
                    subject.add(temp);
                    System.out.println("subject: "+temp);
                    L_SubjectData subjectData = new L_SubjectData();
                    subjectData.setSubject(temp);
                    subjectData.setStdnt_no(stdnt_no);
                    arrayList.add(subjectData);
                    subjectAdapter.notifyDataSetChanged();
                }

            }
        }catch(JSONException e){
            Log.d("","showResult: ",e);
        }
    }
}
