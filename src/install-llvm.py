"""
This file is used to automatic install all of compilers in AutoCBI benchmark
"""
import os










def llvm_install_compilers():
    cmake = '/usr/local/bin/cmake'
    revisions = ["a27b2cac03a180f10e0cc7c5160e9b2625f236bd"]
    # revisions = ["5e37e99ba697487671f713ad62e15b3e9b1faa49", "950f318ff1ab860881f5939cb1cdeef2337e3967",
    #              "79ab7f736fd267665e8b5677f73add15e8c7a7c6", "69b6277a83fd7ee8b0a0ef5e8e52b8c677eda1d6",
    #              "0f328447b638a3518b6edbe28e9bfa252e2c1a7e", "6161b9405fba3aa7b39e599d2873fd62e908b1ec",
    #              "d5b806a27ffb83860a54fe0161ad398388b7278e", "d25789a671c3169412a48c0bacf0ec0c150d5190",
    #              "7915ff34b7022018cf03bf8f18b4a849bfab3b62", "0ac6f9fc6ae5afcc1935638e2a7a3d2c4b150b4f",
    #              "68d2546ec60038956aac096cd72c9547901af257", "60ec3836a2c10cf96526ad499af171f3b1c9b170",
    #              "7fd68d60184c4796c32e9d48363b08d9e0d4c427", "c3fe35df4c2dff728d7fb9db9aee60bd6069cbc8",
    #              "36f974d76babc13a3e1de7b54965583878d5f272", "5af339a1a9139d2b9c04445bb7e38db09c15ad48",
    #              "706f37e8df7b9e18d3f17d18e938d02d0a4d3c47", "3af28945b9cfa8e2264dcb8bdd07aa3e0dc32170",
    #              "e66a7ccf776b8d22819c4baa518a1d5825811c96", "12dd3c4ebb2956413788a301ef0daf48cbbb05d0",
    #              "b16b969d7cd3b135328c0af6f85321d7b134d7fd", "43ab82c562b4b1c22d2ace3cced4cf310a99f206",
    #              "13690037ffcacb740172f1013f1df0e02b62d350", "215f3b7f02e657d56333aa28c89556c523b051a0",
    #              "da0d79e0a0777e8ef81e62d0cc0edb4c82886e15", "49b531a08d13fbb3a2099c7dbb38e212a9735478",
    #              "242ddf4037073da224bb1213751d2f93f3ee1816", "93697fa7557a7305e51c0c5b0982a404d399e6fd",
    #              "0aa1ccb0d91967ea77f83d210609e632234cc8ef", "8287fd8abde6228ebab32953e85c78e75ce0fd30",
    #              "c9f731c47978f7565612c128563466e81d07eb57", "eaa356501dda63182e57e969ab720db617f205b1",
    #              "fae7986bf3cbc89aa56decc576a3700afc022384", "0b2d71373b91f4bf1b0f832ef3e3ab85c3bb1446",
    #              "962932c2e276435e76717a5b0692550abe700026", "6943aa306ee5f27ed3bdd95daa863bed99f2a51b",
    #              "bee9dea306bacdfd7ddf712e8ca38fb5169c8523", "312ff9d19d98b2cb19911fcd0ec7dd378cf8cf1c",
    #              "8e06631b09f7bc735f8753df9e3ffb9818c855d8", "a27b2cac03a180f10e0cc7c5160e9b2625f236bd",
    #              "a27b2cac03a180f10e0cc7c5160e9b2625f236bd.0", "0e83541f8b4e4dc5c69c7048e1c9cb601be06a33",
    #              "79eb3b03660e0056d3153db3e894e675bc5b856a", "dad7cf62de5e8b0b03f8fdd6b6e2da887bfb4892",
    #              "843657c3112660259cb964680b0cfa6eae5052a4", "3f1c0e35e63969c25de3762eb52b7c22d353a73e",
    #              "b93483dbce540b7888df4938dd984955ec8b0343", "3cc265458f9545d126550a55fcbd12778afaedd6",
    #              "3fc0e668ff69bf4dfa8f431b06ba0dd7ef62c751", "75af3af95780e1c379409bf56c516a272c4fa961",
    #              "43e76cd489250329cddb1fd575cf9fc9c17ea334", "719c94a559159cbab9100f0cc6168e9dbd6b8c1f",
    #              "30ffdf42f78c35421f3ea0848846c11b4e36c331", "28bb3d9046fb93bc062a6d0bc514d757e0e352bd",
    #              "d206d6cc5446e6b15ab1795c7d85a63a183057ab", "25090a91bbd77a0bb169ff32e0551be32a7b4c27",
    #              "17d7d145717cc9eedee5f9650f5188a0bf32a65f", "237b218770d8ca14dd0244f6ab889090ce482aae",
    #              "4e971da2723972b589f617301b7c838f00c8e2c7", "a2c5153edd2a4abb4a5a168e28b0be03bdf1f607"]
    # revisions = ['90061908f669864e95715edefa97ab3419bbdb13', '5606dd8a45c5f52074f8afab0e0904595bbf39b2']
    llvm_home = '/data/compilers/llvm'
    revision_dir_pattern = '/data/compilers/llvm/${revision}'
    all_src_dir_pattern = '/data/compilers/llvm/${revision}/${revision}-all'
    simplified_src_dir_pattern = '/data/compilers/llvm/${revision}/${revision}'
    build_dir_pattern = '/data/compilers/llvm/${revision}/${revision}-build'
    repository = '/data/compilers/llvm/llvm-project'
    failed_record = '/data/compilers/llvm/failed_compilers'

    assert len(revisions) == len(list(set(revisions)))

    for r in revisions:
        revision_dir = revision_dir_pattern.replace('${revision}', r)
        all_src_dir = all_src_dir_pattern.replace('${revision}', r)
        simplified_src_dir = simplified_src_dir_pattern.replace('${revision}', r)
        build_dir = build_dir_pattern.replace("${revision}", r)

        real_r = r
        if '.' in r:
            real_r = r.split('.')[0]

        print('==========================================================================')
        os.chdir(llvm_home)
        print('cd ' + llvm_home)

        mkdir_cmd = 'mkdir -p ' + revision_dir
        print(mkdir_cmd)
        if os.system(mkdir_cmd) != 0:
            print('[main] When install ' + r + ', cmd: ' + mkdir_cmd + ' fails')
            #base_layer.put_file_content(failed_record, r + '\t' + mkdir_cmd + '\n')
            continue

        cp_cmd = 'cp -r ' + repository + ' ' + all_src_dir
        print(cp_cmd)
        if os.system(cp_cmd) != 0:
            print('[main] When install ' + r + ', cmd: ' + cp_cmd + ' fails')
           # base_layer.put_file_content(failed_record, r + '\t' + cp_cmd + '\n')
            continue

        os.chdir(all_src_dir)
        print('cd ' + all_src_dir)

        checkout_cmd = 'git checkout ' + real_r
        print(checkout_cmd)
        if os.system(checkout_cmd) != 0:
            print('[main] When install ' + r + ', cmd: ' + checkout_cmd + ' fails')
           # base_layer.put_file_content(failed_record, r + '\t' + checkout_cmd + '\n')
            continue

        # AutoCBI's code, we use recbi's style
        # os.system('svn co http://llvm.org/svn/llvm-project/llvm/trunk -' + rev + ' ' + revpath + '/' + rev)
        # os.system('svn co http://llvm.org/svn/llvm-project/cfe/trunk -' + rev + ' ' + revpath + '/' + rev + '/tools/clang')
        cp_cmd = 'cp -r ' + all_src_dir + '/llvm ' + simplified_src_dir
        print(cp_cmd)
        if os.path.exists(simplified_src_dir) or os.system(cp_cmd) != 0:
            print('[main] When install ' + r + ', cmd: ' + cp_cmd + ' fails')
           # base_layer.put_file_content(failed_record, r + '\t' + cp_cmd + '\n')
            continue

        cp_cmd = 'cp -r ' + all_src_dir + '/clang ' + simplified_src_dir + '/tools/clang'
        print(cp_cmd)
        if os.system(cp_cmd) != 0:
            print('[main] When install ' + r + ', cmd: ' + cp_cmd + ' fails')
           # base_layer.put_file_content(failed_record, r + '\t' + cp_cmd + '\n')
            continue

        mkdir_cmd = 'mkdir -p ' + build_dir
        print(mkdir_cmd)
        if os.system(mkdir_cmd) != 0:
            print('[main] When install ' + r + ', cmd: ' + mkdir_cmd + ' fails')
            #base_layer.put_file_content(failed_record, r + '\t' + mkdir_cmd + '\n')
            continue

        os.chdir(build_dir)
        print('cd ' + build_dir)

        build_cmd = ' '.join([cmake,
                              '-DCMAKE_EXPORT_COMPILER_COMMANDS=ON',
                              '-DCMAKE_INSTALL_PREFIX=' + build_dir,
                              '-DCMAKE_BUILD_TYPE=Release',
                              '-DCMAKE_C_COMPILER=gcc',
                              '-DCMAKE_CXX_COMPILER=g++',
                              '-DCMAKE_C_FLAGS=\"-g -O0 -fprofile-arcs -ftest-coverage\"',
                              '-DCMAKE_CXX_FLAGS=\"-g -O0 -fprofile-arcs -ftest-coverage\"',
                              '-DCMAKE_EXE_LINKER_FLAGS=\"-g -fprofile-arcs -ftest-coverage -lgcov\"',
                              '-DPYTHON_EXECUTABLE:FILEPATH=/usr/bin/python', simplified_src_dir])
        print(build_cmd)
        if os.system(build_cmd) != 0:
            print('[main] When install ' + r + ', cmd: ' + build_cmd + ' fails')
           # base_layer.put_file_content(failed_record, r + '\t' + build_cmd + '\n')
            continue

        make_cmd = 'make -j70'
        print(make_cmd)
        if os.system(make_cmd) != 0:
            print('[main] When install ' + r + ', cmd: ' + make_cmd + ' fails')
           # base_layer.put_file_content(failed_record, r + '\t' + make_cmd + '\n')
            continue

        install_cmd = 'make install'
        print(install_cmd)
        if os.system(install_cmd) != 0:
            print('[main] When install ' + r + ', cmd: ' + install_cmd + ' fails')
          #  base_layer.put_file_content(failed_record, r + '\t' + install_cmd + '\n')
            continue

       # base_layer.safe_rm(all_src_dir)


if __name__ == '__main__':
    # gcc_install_compilers()
    llvm_install_compilers()
