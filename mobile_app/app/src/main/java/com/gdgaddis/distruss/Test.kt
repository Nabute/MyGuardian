//package com.gdgaddis.distruss
//
//import android.content.Intent
//import android.net.Uri
//import android.os.Bundle
//
//
//private fun handleDeepLink(data: Uri?) {
//    when (data?.path) {
//        DeepLink.START -> {
//            // Get the parameter defined as "exerciseType" and add it to the fragment arguments
//            val exerciseType = data.getQueryParameter(DeepLink.Params.ACTIVITY_TYPE).orEmpty()
//            val type = FitActivity.Type.find(exerciseType)
//            val arguments = Bundle().apply {
//                putSerializable(FitTrackingFragment.PARAM_TYPE, type)
//            }
//
//            updateView(FitTrackingFragment::class.java, arguments)
//        }
//        DeepLink.STOP -> {
//            // Stop the tracking service if any and return to home screen.
//            stopService(Intent(this, FitTrackingService::class.java))
//            updateView(FitStatsFragment::class.java)
//        }
//        else -> {
//            // Path is not supported or invalid, start normal flow.
//            showDefaultView()
//        }
//    }
//
//}
//
//
