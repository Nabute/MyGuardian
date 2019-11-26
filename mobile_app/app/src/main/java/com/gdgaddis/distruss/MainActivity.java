package com.gdgaddis.distruss;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.annotation.TargetApi;
import android.content.pm.PackageManager;
import android.content.res.AssetFileDescriptor;
import android.media.MediaRecorder;
import android.os.Build;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.os.Environment;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import org.tensorflow.lite.Interpreter;

import java.io.BufferedInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.util.Random;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    MediaRecorder mediaRecorder;
    TextView counttime;

    boolean stat = false;

    //TODO declaration for Danny's code
    Interpreter tflite;
    String fileName;
    double[] voiceDataNorm;

    String path;

    public int counter;
    private Readable in;

    @TargetApi(Build.VERSION_CODES.O)
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ActivityCompat.requestPermissions(this, new String[] {Manifest.permission.WRITE_EXTERNAL_STORAGE}, PackageManager.PERMISSION_GRANTED);
        ActivityCompat.requestPermissions(this, new String[] {Manifest.permission.RECORD_AUDIO}, PackageManager.PERMISSION_GRANTED);


        Button rec = findViewById(R.id.record);
        rec.setOnClickListener(this);
        Button stop = findViewById(R.id.stop);
        stop.setOnClickListener(this);

        counttime = findViewById(R.id.counttime);

        mediaRecorder = new MediaRecorder();

    }


    public void startRecording(){

        try{

            mediaRecorder.setAudioSource(MediaRecorder.AudioSource.DEFAULT);
            mediaRecorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);

            File path = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);

            Random rand = new Random();
            int a = rand.nextInt();

            File file = new File(path, "/hello.wav");

            mediaRecorder.setOutputFile(file);
            mediaRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);

            mediaRecorder.prepare();
            mediaRecorder.start();

            Toast.makeText(this, "Recording", Toast.LENGTH_LONG).show();

        }catch (Exception e) {
            e.printStackTrace();
        }

    }

    public void stopRecording(){

        Toast.makeText(this, "Recording Saved", Toast.LENGTH_SHORT).show();
        mediaRecorder.stop();
        //mediaRecorder.release();

    }

    @Override
    public void onClick(View v) {
        switch (v.getId()){

            case R.id.record:
                interval();
                break;
            case R.id.stop:
                stopRecording();
                break;

        }
    }


    public void interval(){

        startRecording();
        new CountDownTimer(4000, 1000){
            @Override
            public void onTick(long millisUntilFinished) {
                counttime.setText(String.valueOf(counter));
                counter++;
            }

            @Override
            public void onFinish() {
                counttime.setText("Classifying the Recording");
                stopRecording();

                new CountDownTimer(2000, 1000){
                    @Override
                    public void onTick(long millisUntilFinished) {
                        //do nothing
                        counttime.setText("Preparing for new Recording...");
                        if (checkDistruss()){
                            stat = true;
                        }
                    }

                    @Override
                    public void onFinish() {
                        if (stat=true){
                            //TODO the distruss call will be here
                            //sending sms message or call to a specific phone number stored on the setting of the app
                            //distruss mode ON
                            Toast.makeText(MainActivity.this, "You are in DANGER!!", Toast.LENGTH_SHORT).show();
                        }else{
                            interval();
                        }


                    }
                }.start();

            }
        }.start();
    }


    //TODO Code from Danny

    //to check the distruss read
    public boolean checkDistruss(){
        boolean status = false;

        try {
            tflite = new Interpreter(loadModelFile());

        boolean safelyArrived = false;
        while(true){
            // infinite loop
            //...
            // do some recording
            File path = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
            FileInputStream recodedAudio = new FileInputStream(path.toString() + "hello.3gp");
            /*
            Assuming that the predict function returns 1 if there is a voilence or bad situation or returns 0
            if there is no violence or it is a good situation.
            */
            if(predict(_toByteArray(recodedAudio)) == 1 || safelyArrived){
                // send SMS and finally
                status = true;
                break;
            }else{
                status = false;
            }
        }

        } catch (Exception e) {
            //TODO: handle exception
            e.printStackTrace();
        }



        return status;
    }


    public byte[] _toByteArray(FileInputStream filePath){

        ByteArrayOutputStream arrayOfVoiceData = new ByteArrayOutputStream();
        BufferedInputStream recordedVoice = new BufferedInputStream(filePath);

        int read;
        try {

            byte[] buff = new byte[1024];
            while((read = recordedVoice.read(buff)) > 0) {
                arrayOfVoiceData.write(buff, 0, read);
            }
            arrayOfVoiceData.flush();


        }catch (Exception e){


        }
        byte[] audioByte = arrayOfVoiceData.toByteArray();
        return audioByte;
    }


    public int predict(byte[] voiceData){
        // voiceData might need some normalization
        voiceDataNorm = normalize(voiceData);

        // output shape
        String output = new String();

        // run inference passing the input shape and getting the output shape
        tflite.run(voiceDataNorm, output);

        // get inferred value and return it
        if(output == "bad"){
            return 1;
        }else return 0;
    }

    public double[] normalize(byte[] vector) {
        int listLength = vector.length;
        double[] normalizedVector = new double[vector.length];
        for (int i=0; i<vector.length; i++) {
            normalizedVector[i] = vector[i] / listLength;
        }
        return normalizedVector;
    }

    private MappedByteBuffer loadModelFile() throws IOException {
        // Open the model using an input stream and memory map it to load
        AssetFileDescriptor fileDescriptor = this.getAssets().openFd(fileName= "violence_V2.tflite");
        FileInputStream inputStream = new FileInputStream(fileDescriptor.getFileDescriptor());
        FileChannel fileChannel = inputStream.getChannel();
        long startOffset = fileDescriptor.getStartOffset();
        long declaredLength = fileDescriptor.getDeclaredLength();
        return fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declaredLength);
    }
}
