<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/about', function () {
    return view('about');
});

Route::get('/contact', function () {
    return view('contact');
});

Route::get('/pricing', function () {
    return view('pricing');
});

Route::get('/faq', function () {
    return view('faq');
});

Route::get('/bloghome', function () {
    return view('bloghome');
});

Route::get('/blogpost', function () {
    return view('blogpost');
});

Route::get('/portfoliooverview', function () {
    return view('portfoliooverview');
});

Route::get('/portfolioitem', function () {
    return view('portfolioitem');
});
